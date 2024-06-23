from datetime import datetime

from prisma.models import Case, User
from tux.database.client import db
from tux.utils.enums import CaseType


class CaseController:
    def __init__(self):
        self.table = db.case
        self.users_table = db.user

    async def get_all_cases(self) -> list[Case]:
        return await self.table.find_many()

    async def get_case_by_id(self, case_id: int) -> Case | None:
        return await self.table.find_first(where={"case_id": case_id})

    async def insert_case(
        self,
        guild_id: int,
        case_user_id: int,
        case_moderator_id: int,
        case_type: CaseType,
        case_reason: str,
        case_expires_at: datetime | None = None,
    ) -> Case | None:
        return await self.table.create(
            data={
                "guild_id": guild_id,
                "case_user_id": case_user_id,
                "case_moderator_id": case_moderator_id,
                "case_type": case_type.value,
                "case_reason": case_reason,
                "case_expires_at": case_expires_at,
            }
        )

    async def delete_case_by_id(self, case_id: int) -> None:
        await self.table.delete(where={"case_id": case_id})

    async def update_case_by_id(self, case_id: int, case_reason: str) -> Case | None:
        return await self.table.update(
            where={"case_id": case_id},
            data={"case_reason": case_reason},
        )

    async def get_all_cases_by_user_id(self, case_user_id: int) -> list[Case] | None:
        return await self.table.find_many(where={"case_user_id": case_user_id})

    async def get_all_cases_by_moderator_id(self, case_moderator_id: int) -> list[Case] | None:
        return await self.table.find_many(where={"case_moderator_id": case_moderator_id})

    async def get_all_cases_by_type(self, case_type: CaseType) -> list[Case] | None:
        return await self.table.find_many(where={"case_type": case_type.value})

    async def get_all_cases_by_user_id_and_type(
        self, case_user_id: int, case_type: CaseType
    ) -> list[Case] | None:
        return await self.table.find_many(
            where={"case_user_id": case_user_id, "case_type": case_type.value}
        )

    async def get_all_cases_by_moderator_id_and_type(
        self, case_moderator_id: int, case_type: CaseType
    ) -> list[Case] | None:
        return await self.table.find_many(
            where={"case_moderator_id": case_moderator_id, "case_type": case_type.value}
        )

    async def get_all_cases_by_user_id_and_moderator_id(
        self, case_user_id: int, case_moderator_id: int
    ) -> list[Case] | None:
        return await self.table.find_many(
            where={"case_user_id": case_user_id, "case_moderator_id": case_moderator_id}
        )

    async def get_all_cases_by_user_id_and_moderator_id_and_type(
        self, case_user_id: int, case_moderator_id: int, case_type: CaseType
    ) -> list[Case] | None:
        return await self.table.find_many(
            where={
                "case_user_id": case_user_id,
                "case_moderator_id": case_moderator_id,
                "case_type": case_type.value,
            }
        )

    async def get_last_case_by_user_id(self, case_user_id: int) -> Case | None:
        return await self.table.find_first(
            where={"case_user_id": case_user_id}, order={"case_id": "desc"}
        )

    async def get_last_case_by_user_id_and_type(
        self, case_user_id: int, case_type: CaseType
    ) -> Case | None:
        return await self.table.find_first(
            where={"case_user_id": case_user_id, "case_type": case_type.value},
            order={"case_id": "desc"},
        )

    async def get_last_case_by_moderator_id(self, case_moderator_id: int) -> Case | None:
        return await self.table.find_first(
            where={"case_moderator_id": case_moderator_id}, order={"case_id": "desc"}
        )

    async def get_last_case_by_moderator_id_and_type(
        self, case_moderator_id: int, case_type: CaseType
    ) -> Case | None:
        return await self.table.find_first(
            where={"case_moderator_id": case_moderator_id, "case_type": case_type.value},
            order={"case_id": "desc"},
        )

    async def get_user_from_case_user_id(self, case_id: int) -> User | None:
        case = await self.get_case_by_id(case_id)
        if case:
            return await self.users_table.find_first(where={"user_id": case.case_user_id})
        return None
