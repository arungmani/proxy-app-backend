from app.models.task import TaskModel
from app.db.database import db
from uuid import UUID
from app.services.user_service import get_user_by_id
from app.services.queueService import add_data_to_Broadcastqueue


collection = db.get_collection("tasks_collection")


async def create_task(task_data: TaskModel, sid: str):
    task_dict = task_data.dict(by_alias=True)
    task_dict["_id"] = str(task_dict["_id"])

    result = await collection.insert_one(task_dict)
    return await collection.find_one({"_id": result.inserted_id})


async def list_tasks(user: str, type: str):
    print(user, type)

    # Define a base query
    query = {}

    # Modify the query based on the "type"
    if type == "all_tasks":
        query = {
            "$and": [
                {"created_by": {"$ne": user}},
                {
                    "assignees": {"$ne": user}
                },  # Exclude tasks where the user is already assigned
            ],
            "$or": [
                {"assignees": {"$size": 0}},  # Tasks with no assignees
                {
                    "$expr": {
                        "$lt": [
                            {"$size": "$assignees"},
                            3,
                        ]  # Tasks with fewer than 3 assignees
                    }
                },
            ],
        }
    elif type == "user_tasks":
        query = {"created_by": user}
    elif type == "assigned_tasks":
        query = {
            "assignees": user
        }  # Fetch tasks where the user is one of the assignees
    else:
        # Optionally, handle unknown types
        raise ValueError(f"Unknown task type: {type}")

    # Execute the query
    tasks = await collection.find(query).sort("created_on", -1).to_list(length=100)
    print("THE TASKS IS", tasks)

    return tasks


async def get_task_by_id(task_id: str):

    pipeline = [
        {"$match": {"_id": task_id}},
        {
            "$lookup": {
                "from": "users_collection",  # Name of the users collection
                "localField": "created_by",  # The field in tasks (user_id)
                "foreignField": "_id",  # The field in users (user _id)
                "as": "createdBy",  # Output array name
            }
        },
        {
            "$lookup": {
                "from": "users_collection",  # Name of the users collection
                "localField": "volunteer_id",
                "foreignField": "_id",
                "as": "assignedBy",
            }
        },
        # {
        #     "$unwind": "$user_details",  # Unwind user_details array (optional)
        # },
    ]

    task_with_user_details = await collection.aggregate(pipeline).to_list(length=1)

    if task_with_user_details:
        return task_with_user_details[0]  # Return the task with user details
    return None  # Return None if no task is found


async def update_task_by_id(task_id: str, update_data: dict):
    print("UPDATED DATA", update_data)
    result = await collection.update_one({"_id": task_id}, update_data)
    if result.modified_count == 1:
        return await get_task_by_id(task_id)
    return await get_task_by_id(task_id)


async def delete_task_by_id(task_id: str):
    result = await collection.delete_one({"_id": task_id})
    return result.deleted_count == 1


async def sendBroadcastMessage(task, user_id, sid):
    user = await get_user_by_id(user_id)

    print("THE USER IS", user)

    class Data:
        def __init__(self) -> None:
            self.task_name = task["title"]
            self.user = user["first_name"]
            self.created_at = user["created_on"]
            self.sid = sid

    # Create an instance of the Data class
    data_instance = Data()
    # Print the data attributes
    print("The data is", data_instance.__dict__)

    # Add data to the queue
    add_data_to_Broadcastqueue(data_instance)

    return
