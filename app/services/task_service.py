from app.models.task import TaskModel
from app.db.database import db
from uuid import UUID
from app.services.user_service import get_user_by_id
from app.services.queueService import add_data_to_Broadcastqueue


collection = db.get_collection("tasks_collection")


async def create_task(task_data: TaskModel, sid: str):
    task_dict = task_data.dict(by_alias=True)
    result = await collection.insert_one(task_dict)
    return await collection.find_one({"_id": result.inserted_id})


async def list_tasks(user: str, type: str):
    print(user, type)

    # Handle the "all_tasks" case where both conditions must be satisfied
    if type == "all_tasks":
        tasks = await collection.find(
            {"$and": [{"user_id": {"$ne": user}}, {"volunteer_id": {"$ne": user}}]}
        ).to_list(length=100)
        return tasks

    # Handle the "user_tasks" case
    elif type == "user_tasks":
        user_tasks = await collection.find({"user_id": user}).to_list(length=100)
        return user_tasks

    # Optionally, handle unknown types
    raise ValueError(f"Unknown task type: {type}")


async def get_task_by_id(task_id: UUID):
    return await collection.find_one({"_id": task_id})


async def update_task_by_id(task_id: UUID, update_data: dict):
    print("UPDATED DATA", task_id)
    result = await collection.update_one({"_id": task_id}, {"$set": update_data})
    if result.modified_count == 1:
        return await get_task_by_id(task_id)
    return await get_task_by_id(task_id)


async def delete_task_by_id(task_id: UUID):
    result = await collection.delete_one({"_id": task_id})
    return result.deleted_count == 1




async def sendBroadcastMessage(task, user_id, sid):
    user = await get_user_by_id(UUID(user_id))

    class Data:
        def __init__(self) -> None:
            self.task_name = task["title"]
            self.user = user["first_name"]
            self.sid = sid

    # Create an instance of the Data class
    data_instance = Data()
    # Print the data attributes
    print("The data is", data_instance.__dict__)

    # Add data to the queue 
    add_data_to_Broadcastqueue(data_instance)

    return
