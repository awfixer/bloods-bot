# base embed

from typing import Any

import discord
from discord.ext import commands


class EmbedCreator:
    @staticmethod
    def get_footer(
        ctx: commands.Context[commands.Bot] | None = None,
        interaction: discord.Interaction | None = None,
        fallback_text: str = "tux@atl $",
        fallback_icon_url: str = "https://i.imgur.com/4sblrd0.png",
    ) -> tuple[str, str | None]:
        user: discord.User | discord.Member | None = None
        latency = None

        if ctx:
            user = ctx.author
            latency = round(ctx.bot.latency * 1000, 2)

        elif interaction:
            user = interaction.user
            latency = round(interaction.client.latency * 1000, 2)

        if isinstance(user, discord.User | discord.Member):
            return (
                f"{user.name}@atl $ {latency}ms",
                str(user.avatar.url) if user.avatar else fallback_icon_url,
            )

        return (fallback_text, fallback_icon_url)

    @staticmethod
    def base_embed(
        ctx: commands.Context[commands.Bot] | None,
        interaction: discord.Interaction | None,
        **kwargs: Any,
    ) -> discord.Embed:
        embed = discord.Embed()

        color = kwargs.get("color", kwargs.get("colour", discord.Color.blurple()))
        embed.color = color

        embed.title = kwargs.get("title", "")
        embed.url = kwargs.get("url", "")

        embed.description = kwargs.get("description", "")

        embed.set_image(url=kwargs.get("image_url", ""))
        embed.set_thumbnail(url=kwargs.get("thumbnail_url", ""))

        footer: tuple[str, str | None] = EmbedCreator.get_footer(ctx, interaction)
        embed.set_footer(text=footer[0], icon_url=footer[1])

        embed.timestamp = discord.utils.utcnow()

        return embed

    @staticmethod
    def set_author(embed: discord.Embed, name: str, url: str, icon_url: str) -> None:
        embed.set_author(name=name, url=url, icon_url=icon_url)

    @staticmethod
    def add_field(embed: discord.Embed, name: str, value: str, inline: bool = True) -> None:
        embed.add_field(name=name, value=value, inline=inline)
