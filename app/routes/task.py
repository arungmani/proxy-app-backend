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
from app.services.commentService import delete_comments

router = APIRouter(tags=["Task"], responses={404: {"description": "Not found"}})

# Create Task


@router.post("/task/create", response_model=TaskModel)
async def register_task(
    data: TaskModel, user: dict = Depends(verify_jwt), sid: str = Query(...)
):
    data.created_by = user  # Assuming 'id' is a part of the JWT payload
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
    "/task/get/{id}",
    response_description="Get a single task",
)
async def get_single_task(id: str):
    try:
        task_id = id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    task = await get_task_by_id(task_id)
    print("THE TASK IN ROUTER FUNCTION", task)
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
        task_id, user_id = id, user
        task = await get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

        # Mapping task update actions
        action_map = {
            "assign": lambda: (
                {"$addToSet": {"assignees": user_id}}
                if user_id not in task["assignees"] and len(task["assignees"]) < 3
                else HTTPException(
                    status_code=400,
                    detail="User already assigned or max assignees reached (3)",
                )
            ),
            "unassign": lambda: {"$pull": {"assignees": user_id}},
            "remove_volunteer": lambda: {"$set": {"volunteer_id": None}},
            "update_data": lambda: {
                "$set": {
                    k: v
                    for k, v in task_data.dict(by_alias=True).items()
                    if v is not None and k not in ["_id", "assignees"]
                }
            },
        }

        # Retrieve update action
        filter_data = action_map.get(type, action_map["update_data"])()
        if isinstance(filter_data, HTTPException):
            raise filter_data

        print("THE DATA FOR UPDATION IS", filter_data)

        updated_task = await update_task_by_id(task_id, filter_data)

        if type == "remove_volunteer":
            await delete_comments(
                task["_id"], list(set([task["created_by"], task["volunteer_id"]]))
            )
        if updated_task:
            return updated_task
        else:
            raise HTTPException(status_code=404, detail=f"Task with ID {id} not found")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")


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
