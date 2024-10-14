from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from app.models.task import TaskModel
from app.services.task_service import (
    create_task,
    list_tasks,
    get_task_by_id,
    update_task_by_id,
    delete_task_by_id,
    sendBroadcastMessage,
)
from uuid import UUID
from app.common.helper import verify_jwt
from app.services.queueService import consume_queue

router = APIRouter(tags=["Task"], responses={404: {"description": "Not found"}})

# Create Task


@router.post("/task/create", response_model=TaskModel)
async def register_task(
    data: TaskModel, user: dict = Depends(verify_jwt), sid: str = Query(...)
):
    data.created_by = user  # Assuming 'id' is a part of the JWT payload
    print(data)
    registered_task = await create_task(data, sid)
    await sendBroadcastMessage(registered_task, user, sid)
    return registered_task


# List all tasks


@router.get("/task/list/{type}", response_model=List[TaskModel])
async def list_all_tasks(type: str, user: dict = Depends(verify_jwt)):
    tasks = await list_tasks(user, type)
    return tasks


# Get a single Task


@router.get(
    "/task/get/{id}", response_description="Get a single task", response_model=TaskModel
)
async def get_single_task(id: str):
    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    task = await get_task_by_id(task_id)
    if task:
        return task

    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")


# Update a Task


@router.put(
    "/task/update/{id}", response_description="Update a task", response_model=TaskModel
)
async def update_single_task(
    id: str,
    task_data: TaskModel,
    type: str = Query(...),
    user: dict = Depends(verify_jwt),
):
    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    if type != "assign":
        filter_data = {
            k: v
            for k, v in task_data.dict(by_alias=True).items()
            if v is not None and k != "_id"
        }
    elif type == "assign":
        filter_data = {"volunteer_id": user}
    elif type == "unassign":
        filter_data = {"volunteer_id": None}

    if filter_data:
        updated_task = await update_task_by_id(task_id, filter_data)
        if updated_task:
            return updated_task

    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")


# Delete a Task


@router.delete("/task/delete/{id}")
async def delete_single_task(id: str):
    try:
        task_id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    is_deleted = await delete_task_by_id(task_id)
    if is_deleted:
        return {"message": f"Task with ID {id} has been deleted"}

    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
