from fastapi import APIRouter

router = APIRouter()

@router.get("/home")
async def home():
    return {"message": "welcome to the home page!"}

