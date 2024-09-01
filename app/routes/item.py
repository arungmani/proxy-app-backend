from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.item import ItemModel
from app.db.database import db
from bson import ObjectId

router = APIRouter(
    tags=["Items"],
    responses={404: {"description": "Not found"}}
)

collection = db.get_collection("items_collection")

@router.post("/", response_description="Add new item", response_model=ItemModel)
async def create_item(item: ItemModel):
    item = item.dict(by_alias=True)
    result = await collection.insert_one(item)
    created_item = await collection.find_one({"_id": result.inserted_id})
    return created_item

@router.get("/", response_description="List all items", response_model=List[ItemModel])
async def list_items():
    items = await collection.find().to_list(length=100)

    return items

@router.get("/{id}", response_description="Get a single item", response_model=ItemModel)
async def show_item(id: str):
    if (item := await collection.find_one({"_id": ObjectId(id)})) is not None:
        return item
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")

@router.put("/{id}", response_description="Update an item", response_model=ItemModel)
async def update_item(id: str, item: ItemModel):
    item = {k: v for k, v in item.dict().items() if v is not None}
    if len(item) >= 1:
        update_result = await collection.update_one({"_id": ObjectId(id)}, {"$set": item})
        if update_result.modified_count == 1:
            if (updated_item := await collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_item
    if (existing_item := await collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_item
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")

@router.delete("/{id}", response_description="Delete an item")
async def delete_item(id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Item with ID {id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")