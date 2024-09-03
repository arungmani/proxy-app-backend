from app.models.user import UserModel
from app.db.database import db
from uuid import UUID

collection = db.get_collection("users_collection")

async def create_user(user_data: UserModel):
    user_dict = user_data.dict(by_alias=True)
    result = await collection.insert_one(user_dict)
    return await collection.find_one({"_id": result.inserted_id})

async def list_users():
    return await collection.find().to_list(length=100)

async def get_user_by_id(user_id: UUID):
    return await collection.find_one({"_id": user_id})

async def update_user_by_id(user_id: UUID, update_data: dict):
    result = await collection.update_one({"_id": user_id}, {"$set": update_data})
    if result.modified_count == 1:
        return await get_user_by_id(user_id)
    return await get_user_by_id(user_id)

async def delete_user_by_id(user_id: UUID):
    result = await collection.delete_one({"_id": user_id})
    return result.deleted_count == 1
