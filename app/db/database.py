
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from bson.binary import UuidRepresentation


client = AsyncIOMotorClient(settings.MONGO_URI,uuidRepresentation='standard')
db = client[settings.DATABASE_NAME]