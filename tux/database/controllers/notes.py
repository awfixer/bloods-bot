from prisma.models import Note
from tux.database.client import db


class NoteController:
    def __init__(self):
        self.table = db.note

    async def get_all_notes(self) -> list[Note]:
        return await self.table.find_many()

    async def get_note_by_id(self, note_id: int) -> Note | None:
        return await self.table.find_first(where={"note_id": note_id})

    async def insert_note(
        self,
        note_user_id: int,
        note_moderator_id: int,
        note_content: str,
        guild_id: int,
    ) -> Note:
        return await self.table.create(
            data={
                "note_user_id": note_user_id,
                "note_moderator_id": note_moderator_id,
                "note_content": note_content,
                "guild_id": guild_id,
            }
        )

    async def delete_note_by_id(self, note_id: int) -> None:
        await self.table.delete(where={"note_id": note_id})

    async def update_note_by_id(self, note_id: int, note_content: str) -> Note | None:
        return await self.table.update(
            where={"note_id": note_id},
            data={"note_content": note_content},
        )

    async def get_all_notes_by_user_id(self, note_user_id: int) -> list[Note] | None:
        return await self.table.find_many(where={"note_user_id": note_user_id})

    async def get_all_notes_by_moderator_id(self, note_moderator_id: int) -> list[Note] | None:
        return await self.table.find_many(where={"note_moderator_id": note_moderator_id})

    async def get_all_notes_by_user_id_and_moderator_id(
        self, note_user_id: int, note_moderator_id: int
    ) -> list[Note] | None:
        return await self.table.find_many(
            where={"note_user_id": note_user_id, "note_moderator_id": note_moderator_id}
        )
