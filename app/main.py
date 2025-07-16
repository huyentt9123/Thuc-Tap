from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

app = FastAPI()

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]
users = db["users"]



@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB!"}
