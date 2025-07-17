
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from app.routes import all_routers
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory="templates")
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]
users = db["users"]

# Đưa users collection vào app state để dùng ở router
@app.on_event("startup")
async def startup_event():
    app.state.users = users

# Tự động include tất cả router
for router in all_routers:
    app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <link rel="stylesheet" href="/static/auth.css">
        </head>
        <body>
            <h1 style="color: green;">Hello World</h1>
        </body>
    </html>
    """