from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.user import UserModel
from app.services.user_service import (
    create_user,
    list_users,
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    login_user,
    update_user_ratings,
)
from uuid import UUID
from app.common.helper import verify_jwt
from app.services.redisService import getCache
from app.services.redisService import deleteCache

from pydantic import BaseModel, Field


router = APIRouter(tags=["User"], responses={404: {"description": "Not found"}})

# Register User


class UserListRequest(BaseModel):
    user_ids: List[str]

class RatingReqModel(BaseModel):
    rating:float
    rating_type:str

@router.post("/auth/register", response_model=UserModel)
async def user_registration(data: UserModel):
    registered_user = await create_user(data)
    print("THE REGISTER USER IS", registered_user)
    return registered_user


@router.post(
    "/auth/signin",
)
async def user_signIn(data: UserModel):
    result = await login_user(data)
    return result


# List all users


@router.post(
    "/user/list/all",
)
async def list_all_users(data: UserListRequest):
    print("THE DATA IS ", data)
    users = await list_users(data.user_ids)
    return users


# Get a single User


@router.get(
    "/user/get",
    response_description="Get a single user",
)
async def Ïget_user(
    user: dict = Depends(verify_jwt),
):
    try:
        user_id = user
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = await get_user_by_id(user_id)
    if user:
        # If user exists, retrieve their tifications
        key = f"notifications_{user_id}"  # key for get items from redis
        notifications = await getCache(key)  # get  notifications from redis cache
        # Add notifications as a key in the user dictionary
        user["notifications"] = notifications

        return user

    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")


# Update the user


@router.put(
    "/user/update/{id}", response_description="Update a user", response_model=UserModel
)
async def update_single_user(id: str, user_data: UserModel):
    try:
        user_id = id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    filter_data = {
        k: v
        for k, v in user_data.dict(by_alias=True).items()
        if v is not None and k != "_id"
    }

    if filter_data:
        updated_user = await update_user_by_id(user_id, filter_data)
        if updated_user:
            return updated_user

    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")


# Delete a User


@router.delete("/user/delete/{id}")
async def delete_single_user(id: str):
    try:
        user_id = id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    is_deleted = await delete_user_by_id(user_id)
    if is_deleted:
        return {"message": f"User with ID {id} has been deleted"}

    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")


@router.delete("/user/notifications/delete")
async def delete_user_notifications(user_id: dict = Depends(verify_jwt)):
    try:
        key = f"notifications_{user_id}"  # key for get items from redis
        # Call a different function to handle the deletion
        result = await deleteCache(key)
        if result:
            return {
                "message": f"Notifications for user with ID {user_id} have been deleted"
            }
        else:
            raise HTTPException(
                status_code=404, detail="No notifications found for this user"
            )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred while deleting notifications: {str(e)}",
        )

@router.put("/users/ratings",)
async def update_ratings(
    rating_data: RatingReqModel,  # Expect the entire body as a model
    user_id: dict = Depends(verify_jwt),
):
    """
    Update ratings for a user.

    :param user_id: ID of the user to update ratings for.
    :param rating_data: Object containing the new rating and type.
    :return: Success message or error.
    """
    # Extract rating and type from the model
    rating = rating_data.rating
    rating_type = rating_data.rating_type

    # Validate rating type
    if rating_type not in ["created", "assigned"]:
        raise HTTPException(status_code=400, detail="Invalid rating type.")

    # Call the service to update the ratings
    success = await update_user_ratings(user_id, rating, rating_type)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or update failed.")

    return {"message": f"Rating successfully updated for user {user_id}"}