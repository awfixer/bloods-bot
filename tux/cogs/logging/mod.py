# import discord
# from discord.abc import GuildChannel
# from discord.ext import commands

# from tux.cogs.helpers import Helpers
# from tux.database.controllers import DatabaseController
# from tux.utils.constants import Constants as CONST
# from tux.utils.embeds import EmbedCreator
# from tux.utils.enums import CaseType


# class ModLogging(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot
#         self.mod_log_channel_id: int = CONST.LOG_CHANNELS["MOD"]
#         self.db_controller = DatabaseController()

#     async def send_to_mod_log(self, embed: discord.Embed):
#         channel = self.bot.get_channel(self.mod_log_channel_id)
#         if isinstance(channel, discord.TextChannel):
#             await channel.send(embed=embed)


# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(ModLogging(bot))
