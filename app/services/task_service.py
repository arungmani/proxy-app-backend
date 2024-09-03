from app.models.task import TaskModel
from app.db.database import db
from uuid import UUID

collection = db.get_collection("tasks_collection")

async def create_task(task_data: TaskModel):
    task_dict = task_data.dict(by_alias=True)
    result = await collection.insert_one(task_dict)
    return await collection.find_one({"_id": result.inserted_id})

async def list_tasks():
    return await collection.find().to_list(length=100)

async def get_task_by_id(task_id: UUID):
    return await collection.find_one({"_id": task_id})

async def update_task_by_id(task_id: UUID, update_data: dict):
    result = await collection.update_one({"_id": task_id}, {"$set": update_data})
    if result.modified_count == 1:
        return await get_task_by_id(task_id)
    return await get_task_by_id(task_id)

async def delete_task_by_id(task_id: UUID):
    result = await collection.delete_one({"_id": task_id})
    return result.deleted_count == 1
