from fastapi import APIRouter, HTTPException
from app.models.category import Category
from app.services.category_service import create_category, get_categories
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=str)
async def create_new_category(category: Category):
    category_id = await create_category(category)
    return category_id

@router.get("/", response_model=List[Category])
async def list_categories():
    return await get_categories() 