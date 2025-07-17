from database.database import get_database
from app.models.note import Note
from typing import Optional
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

COLLECTION_NAME = "notes"
db = get_database()
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

async def create_note(note: Note) -> str:
    now = datetime.now(UTC)
    note.created_at = now
    note.updated_at = now
    result = await db[COLLECTION_NAME].insert_one(note.dict(by_alias=True, exclude={"id"}))
    return str(result.inserted_id)

async def get_notes_by_user(user_id: str, category_id: str = None):
    query = {"user_id": user_id}
    if category_id:
        query["category_id"] = category_id
    notes = []
    cursor = db[COLLECTION_NAME].find(query)
    async for document in cursor:
        document["_id"] = str(document["_id"])
        notes.append(Note(**document))
    return notes 