from app.models.user import UserModel
from app.db.database import db
from uuid import UUID
from datetime import datetime
from datetime import timedelta
from fastapi import HTTPException
from typing import List, Optional
import jwt
import bcrypt

collection = db.get_collection("users_collection")


async def create_user(user_data: UserModel):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), salt)
    user_data.password = hashed_password.decode("utf-8")
    user_dict = user_data.dict(by_alias=True)
    user_dict["_id"] = str(user_dict["_id"])

    result = await collection.insert_one(user_dict)
    created_user = await collection.find_one({"_id": result.inserted_id})
    return created_user


async def login_user(credentials):
    user = await collection.find_one({"email": credentials.email})
    if user:
        is_valid = bcrypt.checkpw(
            credentials.password.encode("utf-8"), user["password"].encode("utf-8")
        )
        print(is_valid)
        if is_valid:
            SECRET_KEY = "secret_123"
            payload = {
                "exp": datetime.now() + timedelta(days=15),  # Token expires in 15 days
                "data": str(user["_id"]),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return {"token": token, "user": user}
        # Raise an exception for invalid password
        raise ValueError("Invalid credentials")
    # Raise an exception for user not found
    raise HTTPException(status_code=404, detail=f"user not found")


async def list_users(user_ids: List[str] = None):
    if user_ids:
        print("THE USER IDS IS", user_ids)
        # Fetch users whose IDs match the assignee list (string IDs)
        users = await collection.find({"_id": {"$in": user_ids}}).to_list(length=100)
    else:
        # Fetch all users if no user IDs are provided
        users = await collection.find().to_list(length=100)

    return users


async def get_user_by_id(user_id: str):
    # Retrieve the user from the collection
    return await collection.find_one({"_id": user_id})


async def update_user_by_id(user_id: UUID, update_data: dict):
    result = await collection.update_one({"_id": user_id}, {"$set": update_data})
    if result.modified_count == 1:
        return await get_user_by_id(user_id)
    return await get_user_by_id(user_id)


async def delete_user_by_id(user_id: str):
    result = await collection.delete_one({"_id": user_id})
    return result.deleted_count == 1


async def update_user_ratings(
    user_id: str,
    rating: float,
    rating_type: str,
) -> bool:
    """
    Update the ratings for a user in the database
    """
    user = await get_user_by_id(user_id)
    if not user:
        return False

    if rating_type == "created":
        ratings_field = "created_task_ratings"
        avg_field = "avg_created_task_rating"
    else:
        ratings_field = "assigned_task_ratings"
        avg_field = "avg_assigned_task_rating"

    # Update the ratings array and calculate the new average
    ratings = user.get(ratings_field, [])
    ratings.append(rating)
    avg_rating = sum(ratings) / len(ratings)

    update_result = await update_user_by_id(
        user_id, {ratings_field: ratings, avg_field: avg_rating}
    )
    # db.users.update_one(
    #     {"_id": user_id}, {"$set": {ratings_field: ratings, avg_field: avg_rating}}
    # )
    return update_result
