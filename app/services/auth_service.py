from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(
    users: AsyncIOMotorCollection,
    email: str,
    password: str,
    username: str,
    phone: str = None,
    gender: str = None):
    existing_email = await users.find_one({"email": email})
    if existing_email:
        return False, "Email đã được sử dụng"

    # Kiểm tra trùng username
    existing_username = await users.find_one({"username": username})
    if existing_username:
        return False, "Tên đăng nhập đã tồn tại"

    # Băm mật khẩu
    hashed_password = pwd_context.hash(password)

    # Tạo document người dùng mới
    new_user = {
        "email": email,
        "hashed_password": hashed_password,
        "username": username,
        "phone": phone,
        "gender": gender,
        "created_at": datetime.utcnow(),
    }
    

    # Thêm vào DB
    await users.insert_one(new_user)
    return True, "Đăng ký thành công"

async def login_user(users: AsyncIOMotorCollection, email: str, password: str):
    db_user = await users.find_one({"email": email})
    if not db_user or not pwd_context.verify(password, db_user["hashed_password"]):
        return False, "Invalid credentials"
    return True, "Login successful"
