from datetime import datetime

from prisma.models import GuildUser, User
from prisma.types import UserUpdateInput
from tux.database.client import db


class UserController:
    def __init__(self) -> None:
        self.table = db.user
        self.guild_user_table = db.guilduser

    async def get_all_users(self) -> list[User]:
        return await self.table.find_many()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.table.find_first(where={"user_id": user_id})

    async def insert_user(
        self,
        guild_id: int,
        user_id: int,
        user_name: str | None = None,
        user_bot: bool | None = None,
        user_created_at: datetime | None = None,
        user_joined_at: datetime | None = None,
    ) -> User:
        user = await self.table.upsert(
            where={"user_id": user_id},
            data={
                "create": {
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_bot": user_bot,
                    "user_created_at": user_created_at,
                },
                "update": {},
            },
        )

        # Upsert guild_user relationship
        await self.guild_user_table.upsert(
            where={
                "guild_id_user_id": {
                    "guild_id": guild_id,
                    "user_id": user_id,
                }
            },
            data={
                "create": {
                    "guild_id": guild_id,
                    "user_id": user_id,
                    "user_joined_at": user_joined_at,
                },
                "update": {"user_joined_at": user_joined_at},
            },
        )

        return user

    async def upsert_user_guild_relationship(
        self,
        guild_id: int,
        user_id: int,
        user_joined_at: datetime | None = None,
    ) -> GuildUser:
        return await db.guilduser.upsert(
            where={
                "guild_id_user_id": {
                    "guild_id": guild_id,
                    "user_id": user_id,
                }
            },
            data={
                "create": {
                    "guild_id": guild_id,
                    "user_id": user_id,
                    "user_joined_at": user_joined_at,
                },
                "update": {"user_joined_at": user_joined_at},
            },
        )

    async def update_user_by_id(self, user_id: int, data: UserUpdateInput) -> User | None:
        """
        Example usage:

        ```python
        await user_controller.update_user_by_id(
            user_id=1234567890, data={"user_name": "new name", "user_bot": True}
        )
        ```

        """

        return await self.table.update(where={"user_id": user_id}, data=data)

    async def delete_user_by_id(self, user_id: int) -> None:
        await self.table.delete(where={"user_id": user_id})
