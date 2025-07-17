from database.database import get_database
from app.models.category import Category
from typing import List

COLLECTION_NAME = "categorys"

db = get_database()

async def create_category(category: Category) -> str:
    result = await db[COLLECTION_NAME].insert_one(category.dict(by_alias=True, exclude={"id"}))
    return str(result.inserted_id)

async def get_categories() -> List[Category]:
    categories = []
    cursor = db[COLLECTION_NAME].find()
    async for document in cursor:
        document["_id"] = str(document["_id"]) 
        categories.append(Category(**document))
    return categories 