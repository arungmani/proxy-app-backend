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
    data.created_by =user  # Assuming 'id' is a part of the JWT payload
    registered_task = await create_task(data, sid)
    # await sendBroadcastMessage(registered_task, user, sid)
    return registered_task


# List all tasks


@router.get("/task/list/{type}", response_model=List[TaskModel])
async def list_all_tasks(type: str, user: dict = Depends(verify_jwt)):
    tasks = await list_tasks(user, type)
    return tasks

# Get a single Task

@router.get(
    "/task/get/{id}", response_description="Get a single task", 
)
async def get_single_task(id: str):
    try:
        task_id = id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    task = await get_task_by_id(task_id)
    print("THE TASK IN ROUTER FUNCTION",task)
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
        print("THE TASK ID AND USER ID", id, user)
        task_id = id
        user_id = user
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    if type == "assign":
        # Check if user_id is already in the assignees array
        task = await get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

        if user_id in task['assignees']:
            raise HTTPException(status_code=400, detail=f"User already assigned to this task")

        # Add user_id to the assignees array if there is space (max 3)
        if len(task['assignees']) >= 3:
            raise HTTPException(status_code=400, detail="Task already has maximum number of assignees (3)")

        filter_data = {"$addToSet": {"assignees": user_id}}  # Add user to assignees array

    elif type == "unassign":
        # Remove user_id from the assignees array
        filter_data = {"$pull": {"assignees": user_id}}

    else:
        # Update other task data
        filter_data = {
          "$set": {
            k: v
            for k, v in task_data.dict(by_alias=True).items()
            if v is not None and k != "_id" and k != "assignees"
        }
        }

    print("THE DATA FOR UPDATION IS", filter_data)

    if filter_data:
        updated_task = await update_task_by_id(task_id, filter_data)
        if updated_task:
            return updated_task

    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

# Delete a Task


@router.delete("/task/delete/{id}")
async def delete_single_task(id: str):
    try:
        task_id = id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    is_deleted = await delete_task_by_id(task_id)
    if is_deleted:
        return {"message": f"Task with ID {id} has been deleted"}

    raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")
    