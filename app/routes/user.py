from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.user import UserModel
from app.db.database import db
from bson import ObjectId

router = APIRouter(
    tags=["User"],
    responses={404: {"description": "Not found"}}
)

collection = db.get_collection("users_collection")

# Register User

@router.post('/user/register',response_model=UserModel)
async def user_registration(data: UserModel):
    userData= data.dict(by_alias=True)
    result = await collection.insert_one(userData)
    registered_user = await collection.find_one({"_id": result.inserted_id})
    return registered_user


# List all users

@router.get("/user/list" ,response_model=List[UserModel])
async def list_users():
    users = await collection.find().to_list(length=100)
    return users
 

# Get a single User

@router.get("/user/get/{id}", response_description="Get a single item", response_model=UserModel)
async def get_user(id: str):
    if (user:= await collection.find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")


# Update the user

@router.put("/user/update/{id}", response_description="Update an user", response_model=UserModel)
async def update_item(id: str, userData: UserModel):
    filterData = {k: v for k, v in userData.dict().items() if v is not None}
    if len(filterData) >= 1:
        update_result = await collection.update_one({"_id": ObjectId(id)}, {"$set": filterData})
        if update_result.modified_count == 1:
            if (updated_user := await collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_user
    if (existing_item := await collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_item
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")



# Delete a User

@router.delete("/user/delete/{id}")
async def delete_user(id:str):
    delete_result=await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Item with ID {id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
  