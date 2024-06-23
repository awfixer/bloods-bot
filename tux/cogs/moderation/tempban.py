from datetime import UTC, datetime, timedelta

import discord
from discord.ext import commands

from tux.database.controllers import DatabaseController
from tux.handlers.infractions import handle_infraction
from tux.utils.enums import InfractionType
from tux.utils.flags import TempBanFlags


class TempBan(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db_controller = DatabaseController()

    @commands.hybrid_command(
        name="temp_ban",
        description="Issues a temporary ban to a member of the server.",
        aliases=["tb", "tban"],
        usage="$tempban @member -r foo -d 30 -p 1",
    )
    async def temp_ban(
        self,
        ctx: commands.Context[commands.Bot],
        member: discord.Member,
        *,
        flags: TempBanFlags,
    ) -> None:
        expires_at = datetime.now(UTC) + timedelta(days=flags.expires_at)

        await handle_infraction(
            self.db_controller,
            ctx,
            member,
            flags.reason,
            InfractionType.TEMP_BAN,
            expires_at=expires_at,
            purge_days=flags.purge_days,
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TempBan(bot))
