from pydantic import BaseModel

class Settings(BaseModel):
    MONGODB_URL: str = "mongodb+srv://hien123:hien123@cluster0.zoc2tr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    DATABASE_NAME: str = "data"
    class Config:
        env_file = ".env"
settings = Settings()
