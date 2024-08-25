import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://mongo:27017/test_db")
    DATABASE_NAME: str = "test_db"

settings = Settings()