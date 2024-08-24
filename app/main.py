from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import Optional

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
DATABASE_NAME = "test"
db = client[DATABASE_NAME]

COLLECTION_NAME = "items"
collection = db[COLLECTION_NAME]

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    result = collection.insert_one(item.dict())
    # Enqueue the task with the correct argument
    return {"id": str(result.inserted_id)}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    obj_id = ObjectId(item_id)
    item = collection.find_one({"_id": obj_id})
    if item:
        return {"name": item["name"], "description": item.get("description")}
    return {"error": "Item not found"}
