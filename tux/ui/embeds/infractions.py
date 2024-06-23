# Base embed for infraction embeds

from typing import Any

import discord
from discord.ext import commands

from prisma.models import Infractions
from tux.utils.constants import Constants as CONST

from . import EmbedCreator


class InfractionEmbeds:
    # Base embed for infraction embeds

    @staticmethod
    def base_embed(
        ctx: commands.Context[commands.Bot] | None,
        interaction: discord.Interaction | None,
        infraction: Infractions,
        **kwargs: Any,
    ) -> discord.Embed:
        embed = EmbedCreator.base_embed(ctx, interaction, color=CONST.COLORS["INFRACTION"])

        user = kwargs.get("user", None)

        embed.set_author(name=f"Case {infraction.id}", icon_url=CONST.ICONS["INFRACTION"], url="")

        embed.add_field(name="User", value=f"{user.mention} ({user.id})", inline=False)

        return embed

    # Ban embed

    # Temp ban embed

    # Unban embed

    # Kick embed

    # Mute embed

    # Timeout embed

    # Warn embed
