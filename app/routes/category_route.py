from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from app.models.category import Category
from app.services.category_service import create_category, get_categories_for_user
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=str)
async def create_new_category(
    request: Request,
    name: str = Form(...),
    description: str = Form(None)
):
    user = request.session.get("user")
    user_id = user["id"] if user and user.get("id") else None
    category = Category(name=name, description=description, user_id=user_id)
    await create_category(category)
    return RedirectResponse(url="/home", status_code=303)

@router.get("/", response_model=List[Category])
async def list_categories(request: Request):
    user = request.session.get("user")
    user_id = user["id"] if user and user.get("id") else None
    return await get_categories_for_user(user_id) 