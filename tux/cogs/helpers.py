# import discord
# from discord.ext import commands
# from loguru import logger

# from prisma.models import User
# from tux.database.controllers import DatabaseController
# from tux.utils.constants import Constants as CONST


# class Helpers(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot

#     async def get_guild_from_int(self, guild_id: int) -> discord.Guild | None:
#         try:
#             guild = self.bot.get_guild(guild_id)
#         except Exception as error:
#             logger.error(f"Failed to get guild from id. Error: {error}")
#             return None

#         return guild

#     async def get_or_fetch_member(
#         self, guild: discord.Guild | None, user_id: int
#     ) -> discord.Member | None:
#         if not guild:
#             return None

#         member = guild.get_member(user_id)

#         if not member:
#             try:
#                 member = await guild.fetch_member(user_id)
#             except (discord.HTTPException, discord.NotFound, discord.Forbidden):
#                 return None

#         return member

#     async def get_member_from_ctx(
#         self, ctx: commands.Context[commands.Bot]
#     ) -> discord.Member | None:
#         if ctx.guild:
#             member = ctx.guild.get_member(ctx.author.id)
#             if not member:
#                 try:
#                     member = await ctx.guild.fetch_member(ctx.author.id)
#                 except (discord.HTTPException, discord.NotFound, discord.Forbidden):
#                     return None
#             return member
#         return None

#     async def get_or_insert_user(
#         self,
#         db_controller: DatabaseController,
#         user: discord.User | discord.Member,
#     ) -> User | None:
#         guild_id = user.guild.id if isinstance(user, discord.Member) else 0

#         try:
#             record = await db_controller.users.get_user_by_id(
#                 user.id
#             ) or await db_controller.users.insert_user(
#                 user_id=user.id,
#                 user_name=user.name,
#                 user_bot=user.bot,
#                 user_created_at=user.created_at,
#                 guild_id=guild_id,
#             )

#         except Exception as error:
#             logger.error(f"Failed to get or insert user. Error: {error}")
#             return None

#         return record

#     async def get_or_insert_moderator(
#         self, db_controller: DatabaseController, user: discord.User | discord.Member
#     ) -> User | None:
#         guild_id = user.guild.id if isinstance(user, discord.Member) else 0

#         try:
#             record = await db_controller.users.get_user_by_id(
#                 user.id
#             ) or await db_controller.users.insert_user(
#                 user_id=user.id,
#                 user_name=user.name,
#                 user_bot=user.bot,
#                 user_created_at=user.created_at,
#                 guild_id=guild_id,
#             )

#         except Exception as error:
#             logger.error(f"Failed to get or insert moderator. Error: {error}")
#             return None

#         return record


# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(Helpers(bot))
