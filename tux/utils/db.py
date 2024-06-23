import discord
from loguru import logger

from prisma.models import User
from tux.database.controllers import DatabaseController
from tux.utils.constants import Constants as CONST
from tux.utils.functions import get_or_fetch_member


async def get_or_insert_user(
    db_controller: DatabaseController,
    user: discord.User | discord.Member,
) -> User | None:
    try:
        member = await get_or_fetch_member(CONST.PROD_GUILD_ID, user.id)
    except Exception as error:
        logger.error(f"Failed to get or fetch member. Error: {error}")
        return None

    try:
        record = await db_controller.users.get_user_by_id(
            user.id
        ) or await db_controller.users.insert_user(
            user_id=user.id,
            user_name=user.name,
            user_bot=user.bot,
            user_created_at=user.created_at,
            user_guild_id=user.guild.id,
        )

    except Exception as error:
        logger.error(f"Failed to get or insert user. Error: {error}")
        return None

    return record


async def get_or_insert_moderator(
    db_controller: DatabaseController, user: discord.User | discord.Member
) -> User | None:
    try:
        record = await db_controller.users.get_user_by_id(
            user.id
        ) or await db_controller.users.insert_user(
            user_id=user.id,
            user_name=user.name,
            user_bot=user.bot,
            user_created_at=user.created_at,
        )

    except Exception as error:
        logger.error(f"Failed to get or insert moderator. Error: {error}")
        return None

    return record
