from fastapi import APIRouter, HTTPException, status,Depends
from typing import List
from app.models.user import UserModel
from app.services.user_service import (
    create_user,
    list_users,
    get_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    login_user
)
from uuid import UUID
from app.common.helper import verify_jwt


router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}}
)

# Register User

@router.post('/user/register', response_model=UserModel)
async def user_registration(data: UserModel):
    print("THE DATA IA",data)
    registered_user = await create_user(data)
    return registered_user

@router.post("/user/signin",)
async def user_signIn(data:UserModel):
    result=await login_user(data)
    return result

# List all users

@router.get("/user/list", response_model=List[UserModel])
async def list_all_users():
    users = await list_users()
    return users

# Get a single User

@router.get("/user/get", response_description="Get a single user",)
async def get_user(user: dict = Depends(verify_jwt),
):
    try:
        user_id = UUID(user)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    user = await get_user_by_id(user_id)
    if user:
        return user
    
    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")

# Update the user

@router.put("/user/update/{id}", response_description="Update a user", response_model=UserModel)
async def update_single_user(id: str, user_data: UserModel):
    try:
        user_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    filter_data = {k: v for k, v in user_data.dict(by_alias=True).items() if v is not None and k != "_id"}
    
    if filter_data:
        updated_user = await update_user_by_id(user_id, filter_data)
        if updated_user:
            return updated_user
    
    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")

# Delete a User

@router.delete("/user/delete/{id}")
async def delete_single_user(id: str):
    try:
        user_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    is_deleted = await delete_user_by_id(user_id)
    if is_deleted:
        return {"message": f"User with ID {id} has been deleted"}
    
    raise HTTPException(status_code=404, detail=f"User with ID {id} not found")
