import discord
from discord.ext import commands

from prisma.models import Case, User
from tux.database.controllers import DatabaseController
from tux.utils.constants import Constants as CONST
from tux.utils.embeds import EmbedCreator
from tux.utils.enums import CaseType

db_controller = DatabaseController()


async def send_temporary_message(ctx: commands.Context[commands.Bot], message: str) -> None:
    await ctx.send(message, ephemeral=True, delete_after=5)


async def send_embed_to_mod_log(
    ctx: commands.Context[commands.Bot],
    mod_log_channel_id: int,
    embed: discord.Embed,
) -> None:
    if (
        ctx.guild
        and (mod_log_channel := ctx.guild.get_channel(mod_log_channel_id))
        and isinstance(mod_log_channel, discord.TextChannel)
    ):
        await mod_log_channel.send(embed=embed)


def create_mod_log_embed(
    ctx: commands.Context[commands.Bot],
    title: str,
    color: int | discord.Color,
    author_icon_url: str = CONST.ICONS["SUCCESS"],
) -> discord.Embed:
    embed = EmbedCreator.create_embed(ctx, title=title)
    embed.color = color
    embed.set_author(name=title, icon_url=author_icon_url)
    return embed


async def insert_user_and_moderator(
    target: discord.Member, ctx: commands.Context[commands.Bot]
) -> tuple[User, User] | None:
    if ctx.guild:
        target_record = await db_controller.users.insert_user(
            user_id=target.id, user_name=target.name, guild_id=ctx.guild.id
        )
        moderator_record = await db_controller.users.insert_user(
            user_id=ctx.author.id,
            user_name=ctx.author.name,
            guild_id=ctx.guild.id,
        )
        return target_record, moderator_record
    return None


async def insert_case(
    target: discord.Member, ctx: commands.Context[commands.Bot], case_type: CaseType, reason: str
) -> Case | None:
    if ctx.guild:
        return await db_controller.cases.insert_case(
            guild_id=ctx.guild.id,
            case_user_id=target.id,
            case_moderator_id=ctx.author.id,
            case_type=case_type,
            case_reason=reason,
        )
    return None


async def cleanup_failed_case(case: Case | None) -> None:
    if case:
        await db_controller.cases.delete_case_by_id(case.case_id)
