from app.models.user import UserModel
from app.db.database import db
from uuid import UUID
from datetime import datetime
from datetime import timedelta
from fastapi import  HTTPException


import jwt
import bcrypt

collection = db.get_collection("users_collection")





async def create_user(user_data: UserModel):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt)
    user_data.password=hashed_password.decode('utf-8')
    user_dict = user_data.dict(by_alias=True)
    result = await collection.insert_one(user_dict)
    created_user=await collection.find_one({"_id": result.inserted_id})
    return created_user


async def login_user(credentials):
    user = await collection.find_one({"email": credentials.email})
    if user:
        is_valid = bcrypt.checkpw(credentials.password.encode('utf-8'), user['password'].encode('utf-8'))
        print(is_valid)
        if is_valid:
            SECRET_KEY = "secret_123"
            payload = {
                "exp":datetime.now()+timedelta(days=15), # Token expires in 15 days
                "data": str(user['_id']) 
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return {"token": token} 
        # Raise an exception for invalid password
        raise ValueError("Invalid credentials")
    # Raise an exception for user not found
    raise HTTPException(status_code=404, detail=f"user not found")


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
