import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from prisma.models import Infractions
from tux.database.controllers import DatabaseController
from tux.utils.embeds import EmbedCreator
from tux.utils.enums import InfractionType


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db_controller = DatabaseController()

    async def insert_infraction(
        self,
        user_id: int,
        moderator_id: int,
        infraction_type: InfractionType,
        infraction_reason: str,
    ) -> Infractions | None:
        """
        Inserts a new infraction into the database.

        Parameters
        ----------
        user_id : int
            The ID of the user for whom the infraction is created.
        moderator_id : int
            The ID of the moderator who created the infraction.
        infraction_type : InfractionType
            The type of the infraction.
        infraction_reason : str
            The reason for the infraction.

        Returns
        -------
        Infractions | None
            The newly created infraction if successful, otherwise None.
        """

        try:
            return await self.db_controller.infractions.create_infraction(
                user_id=user_id,
                moderator_id=moderator_id,
                infraction_type=infraction_type,
                infraction_reason=infraction_reason,
            )

        except Exception as error:
            logger.error(f"Failed to create infraction for user {user_id}. Error: {error}")
            return None

    async def get_or_create_user(self, member: discord.Member) -> None:
        """
        Retrieves or creates a user in the database.

        Parameters
        ----------
        member : discord.Member
            The member to retrieve or create in the database.
        """

        user = await self.db_controller.users.get_user_by_id(member.id)

        if not user:
            await self.db_controller.users.create_user(
                user_id=member.id,
                name=member.name,
                display_name=member.display_name,
                mention=member.mention,
                bot=member.bot,
                created_at=member.created_at,
                joined_at=member.joined_at,
            )

    async def get_or_create_moderator(self, interaction: discord.Interaction) -> None:
        """
        Retrieves or creates a moderator in the database.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction to retrieve or create the moderator from.
        """

        moderator = await self.db_controller.users.get_user_by_id(interaction.user.id)
        moderator_context = None
        if interaction.guild:
            moderator_context = interaction.guild.get_member(interaction.user.id)

        if not moderator:
            await self.db_controller.users.create_user(
                user_id=interaction.user.id,
                name=interaction.user.name,
                display_name=interaction.user.display_name,
                mention=interaction.user.mention,
                bot=interaction.user.bot,
                created_at=interaction.user.created_at,
                joined_at=moderator_context.joined_at if moderator_context else None,
            )

    @app_commands.checks.has_any_role("Root", "Admin", "Sr. Mod", "Mod")
    @app_commands.command(name="ban", description="Issues a ban to a member of the server.")
    @app_commands.describe(member="The member to ban", reason="The reason for issuing the ban")
    async def ban(
        self, interaction: discord.Interaction, member: discord.Member, reason: str | None = None
    ) -> None:
        """
        Issues a ban to a member of the server.

        Parameters
        ----------
        interaction : discord.Interaction
            The interaction that triggered the command.
        member : discord.Member
            The member to ban.
        reason : str | None, optional
            The reason for issuing the ban, by default None.
        """

        reason = reason or "No reason provided"

        await self.get_or_create_user(member)
        await self.get_or_create_moderator(interaction)

        try:
            await member.ban(reason=reason)

            new_ban = await self.insert_infraction(
                user_id=member.id,
                moderator_id=interaction.user.id,
                infraction_type=InfractionType.BAN,
                infraction_reason=reason,
            )

            ban_id = new_ban.id if new_ban else "Unknown"

            embed = EmbedCreator.create_infraction_embed(
                title="",
                description="",
                interaction=interaction,
            )
            embed.add_field(name="Action", value="Ban", inline=True)
            embed.add_field(name="Case ID", value=f"`{ban_id}`", inline=True)
            embed.add_field(name="Reason", value=f"`{reason}`", inline=False)
            embed.add_field(name="Moderator", value=f"{interaction.user.display_name}", inline=True)

            logger.info(f"Ban issued to {member.display_name} ({member.id}) for: {reason}")

        except Exception as error:
            msg = f"Failed to issue ban to {member.display_name}."
            embed = EmbedCreator.create_error_embed(
                title="Ban Failed",
                description=msg,
                interaction=interaction,
            )

            logger.error(f"{msg} Error: {error}")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))
