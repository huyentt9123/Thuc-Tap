from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://hien123:hien123@cluster0.zoc2tr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME: str = "note_db"

settings = Settings()
