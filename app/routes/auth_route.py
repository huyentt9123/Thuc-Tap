from fastapi import APIRouter, HTTPException, status, Depends, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.models.user import UserCreate, UserLogin
from motor.motor_asyncio import AsyncIOMotorCollection
from app.services.auth_service import register_user, login_user

router = APIRouter() 
templates = Jinja2Templates(directory="app/templates")

# Helper to get users collection
# Helper to get users collection
def get_users_collection(request: Request) -> AsyncIOMotorCollection:
    return request.app.state.users

# Route render giao diện đăng ký
@router.get("/auth/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("auth_template.html", {"request": request, "form_type": "register", "error": None})

# Route render giao diện đăng nhập
@router.get("/auth/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("auth_template.html", {"request": request, "form_type": "login", "error": None})

@router.post("/auth/register", status_code=201)
async def register(request: Request, user: UserCreate = Body(...)):
    users = get_users_collection(request)

    success, message = await register_user(
        users=users,
        email=user.email,
        password=user.password,
        username=user.username,
        phone=user.phone,
        gender=user.gender
    )
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"msg": message}


# Xử lý đăng nhập từ form HTML
from fastapi import Form

@router.post("/auth/login")
async def login_api(request: Request,user: UserLogin = Body(...)):
    users = get_users_collection(request)
    success, message, db_user = await login_user(users, user.email, user.password)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    # Lưu thông tin user vào session
    request.session["user"] = {"email": db_user["email"], "id": str(db_user["_id"])}
    return {"msg": message}


