from pydantic import BaseModel, EmailStr, Field

from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    phone: Optional[str] = None
    gender: Optional[str] = None  # "male", "female", "other"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# class UserInDB(BaseModel):
#     email: EmailStr
#     hashed_password: str