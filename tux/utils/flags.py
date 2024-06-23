from discord.ext import commands


class BanFlags(commands.FlagConverter, delimiter=" ", prefix="-"):
    reason: str = commands.flag(
        name="reason",
        description="The reason for the member ban.",
        aliases=["r"],
        default="No reason provided.",
    )
    purge_days: int = commands.flag(
        name="purge_days",
        description="The number of days (< 7) to purge in messages.",
        aliases=["p"],
        default=0,
    )


class TempBanFlags(commands.FlagConverter, delimiter=" ", prefix="-"):
    reason: str = commands.flag(
        name="reason",
        description="The reason for the member temp ban.",
        aliases=["r"],
        default="No reason provided.",
    )
    expires_at: int = commands.flag(
        name="expires_at",
        description="The time in days the ban will last for.",
        aliases=["t", "d", "e"],
    )
    purge_days: int = commands.flag(
        name="purge_days",
        description="The number of days (< 7) to purge in messages.",
        aliases=["p"],
        default=0,
    )
