from app.models.comment import CommentsModel
from app.db.database import db
from uuid import UUID
from fastapi import HTTPException
from pymongo import DESCENDING
from app.services.task_service import get_task_by_id
from typing import Optional
from app.services.socket import send_message_to_room


collection = db.get_collection("comments_collection")


async def createComment(comment: CommentsModel):
    try:
        comment_dict = comment.dict(by_alias=True)
        comment_dict["_id"] = str(comment_dict["_id"])
        result = await collection.insert_one(comment_dict)

        if comment_dict["parent_id"]:
            comment_id = comment_dict["parent_id"]
            await updateComment(comment_id, {"hasReplies": True})
        await showRealTimeCommentNotification(
            comment.sender["user_id"], comment.task_id
        )
        return await getSingleComment(result.inserted_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def getComments(task_id: str, parent_id: Optional[str] = None):
    try:
        task = await get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Collect relevant user IDs and remove duplicates
        user_ids = list(set([task["volunteer_id"], task["created_by"]]))

        # Build the match filter
        match_filter = {
            "sender.user_id": {"$in": user_ids},  # Changed to match sender.user_id
            "task_id": task_id,
        }
        # Add parent_id conditionally
        if parent_id is not None:
            match_filter["parent_id"] = parent_id

        # Define the aggregation pipeline
        pipeline = [{"$match": match_filter}, {"$sort": {"created_at": DESCENDING}}]

        # Execute the query and return results
        return await collection.aggregate(pipeline).to_list(length=100)

    except HTTPException as e:
        raise e  # Re-raise HTTP exceptions as-is
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving comments."
        )


async def getSingleComment(id: str):
    try:
        # Define the aggregation pipeline
        pipeline = [
            {"$match": {"_id": id}},  # Match the comment by its ID
            {
                "$lookup": {
                    "from": "users_collection",  # The users collection to join
                    "localField": "user_id",  # The field in the comments collection
                    "foreignField": "_id",  # The field in the users collection
                    "as": "sendBy",  # The output array
                }
            },
            {"$limit": 1},  # Since we are looking for a single comment
        ]

        # Run the aggregation query
        result = await collection.aggregate(pipeline).to_list(length=1)

        if not result:
            raise HTTPException(status_code=404, detail="Comment not found")

        return result[0]  # Return the single comment

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def updateComment(comment_id: str, update_data: dict):
    try:
        comment_dict = update_data.dict(by_alias=True)
        filter_data = {
            k: v for k, v in comment_dict.items() if v is not None and k != "_id"
        }

        if filter_data:
            await collection.update_one({"_id": comment_id}, {"$set": filter_data})

        return await getSingleComment(comment_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def deleteSingleComment(comment_id):
    try:
       result=await collection.delete_one({"_id": comment_id})
       return result.deleted_count == 1
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting comments."
        )


async def delete_comments(task_id: str, user_ids: list[str]):
    try:
        print("THE TASK ID AND USER IDS IS", task_id, user_ids)
        # Build the filter for deletion
        delete_filter = {
            "task_id": task_id,
            "sender.user_id": {"$in": user_ids},  # Match any of the specified user IDs
        }

        # Execute the delete operation
        result = await collection.delete_many(delete_filter)

        # Return the number of deleted documents for confirmation
        return {"deleted_count": result.deleted_count}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting comments."
        )


async def showRealTimeCommentNotification(sender_id: str, task_id: str):
    task = await get_task_by_id(task_id)
    if task["volunteer_id"] != sender_id:
        # Send message to the volunteer's room
        await send_message_to_room(task["volunteer_id"], "create the comment")
        print("WORKING FIRST CONDITION")
    else:
        # Send message to the creator's room
        await send_message_to_room(
            task["created_by"],
            "create the comment",
        )
        print("WORKING THE SECOND CONDITION")
