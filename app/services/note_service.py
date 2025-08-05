from database.database import get_database
from app.models.note import Note
from typing import Optional
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from bson import ObjectId
from bson.errors import InvalidId

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

async def delete_note(note_id: str) -> bool:
    try:
        obj_id = ObjectId(note_id)
    except (InvalidId, TypeError):
        print(f"[ERROR] Invalid note_id: {note_id}")
        return False
    result = await db[COLLECTION_NAME].delete_one({"_id": ObjectId(note_id)})
    return result.deleted_count == 1 


async def update_note(note_id: str, title: str, content: str, category_id: str) -> bool:
    try:
        obj_id = ObjectId(note_id)
    except (InvalidId, TypeError):
        print(f"[ERROR] Invalid note_id: {note_id}")
        return False
    result = await db[COLLECTION_NAME].update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"title": title, "content": content, "category_id": category_id}}
    )
    return result.modified_count == 1


async def get_note_by_id(note_id: str):
    try:
        obj_id = ObjectId(note_id)
    except (InvalidId, TypeError):
        print(f"[ERROR] Invalid note_id: {note_id}")
        return False
    document = await db[COLLECTION_NAME].find_one({"_id": ObjectId(note_id)})
    if document:
        document["_id"] = str(document["_id"])
        return Note(**document)
    return None 

