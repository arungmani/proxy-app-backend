
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from bson.binary import UuidRepresentation


client = AsyncIOMotorClient(settings.MONGO_URI,uuidRepresentation='standard')
db = client[settings.DATABASE_NAME]


async def initialize_indexes():
    """Create all required indexes"""
    await db.tasks_collection.create_index([("location", "2dsphere")])


