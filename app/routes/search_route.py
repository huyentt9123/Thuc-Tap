from fastapi import APIRouter, Query, Request
from app.services.search_service import search_notes_in_es

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
async def search_notes(request: Request, q: str = Query(...)):
    user = request.session.get("user")
    user_id = user["id"] if user and user.get("id") else None
    return await search_notes_in_es(q, user_id)