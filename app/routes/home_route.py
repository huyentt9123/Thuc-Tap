from fastapi import APIRouter, Request, Depends, Form, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.category_service import get_categories
from typing import List
from app.services.note_service import create_note
from app.models.note import Note
from app.services.note_service import get_notes_by_user
from app.services.note_service import delete_note
from app.services.note_service import update_note
from zoneinfo import ZoneInfo
from app.services.note_service import get_note_by_id

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request, category_id: str = Query(None), edit_id: str = Query(None)):
    user = request.session.get("user")
    if not user or not user.get("id"):
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    user_id = user.get("id")
    categories = await get_categories()
    notes = await get_notes_by_user(user_id, category_id)
    vn_tz = ZoneInfo("Asia/Ho_Chi_Minh")
    for note in notes:
        if hasattr(note, 'created_at') and note.created_at:
            # Nếu là string ISO, parse sang datetime
            from datetime import datetime
            if isinstance(note.created_at, str):
                try:
                    note.created_at = datetime.fromisoformat(note.created_at.replace('Z', '+00:00'))
                except Exception:
                    note.created_at = None
            if note.created_at and note.created_at.tzinfo is None:
                note.created_at = note.created_at.replace(tzinfo=ZoneInfo("UTC"))
            if note.created_at:
                note.created_at = note.created_at.astimezone(vn_tz)
    note_to_edit = None
    if edit_id:
        note_to_edit = await get_note_by_id(edit_id)
    return templates.TemplateResponse(
        "home_template.html",
        {"request": request, "categories": categories, "notes": notes, "selected_category": category_id, "note_to_edit": note_to_edit}
    )


@router.post("/notes/create")
async def create_note_route(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category_id: str = Form(...)
):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    user_id = user.get("id")  # hoặc user.get("id") nếu bạn lưu id
    note = Note(title=title, content=content, user_id=user_id, category_id=category_id)
    await create_note(note)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/notes/delete")
async def delete_note_route(request: Request, note_id: str = Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    await delete_note(note_id)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

from app.services.note_service import update_note  # Đảm bảo dòng này có

@router.post("/notes/update")
async def update_note_route(
    request: Request,
    note_id: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    category_id: str = Form(...)
):
    await update_note(note_id=note_id, title=title, content=content, category_id=category_id)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
