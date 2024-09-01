from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.task import TaskModel
from app.db.database import db
from bson import ObjectId

router = APIRouter(
    tags=["Task"],
    responses={404: {"description": "Not found"}}
)

collection = db.get_collection("tasks_collection")

# Create Task

@router.post('/task/create', response_model=TaskModel)
async def register_task(data: TaskModel):
    task_data = data.dict(by_alias=True)
    result = await collection.insert_one(task_data)
    registered_task = await collection.find_one({"_id": result.inserted_id})
    return registered_task

# List all tasks

@router.get("/task/list", response_model=List[TaskModel])
async def list_tasks():
    tasks = await collection.find().to_list(length=100)
    return tasks

# Get a single Task

@router.get("/task/get/{id}", response_description="Get a single task", response_model=TaskModel)
async def get_task(id: str):
    if (task := await collection.find_one({"_id": ObjectId(id)})) is not None:
        return task
    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

# Update a Task

@router.put("/task/update/{id}", response_description="Update a task", response_model=TaskModel)
async def update_task(id: str, task_data: TaskModel):
    filter_data = {k: v for k, v in task_data.dict(by_alias=True).items() if v is not None}
    if filter_data:
        update_result = await collection.update_one({"_id": ObjectId(id)}, {"$set": filter_data})
        if update_result.modified_count == 1:
            if (updated_task := await collection.find_one({"_id": ObjectId(id)})) is not None:
                return updated_task
    if (existing_task := await collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_task
    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

# Delete a Task

@router.delete("/task/delete/{id}")
async def delete_task(id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Task with ID {id} has been deleted"}
    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
