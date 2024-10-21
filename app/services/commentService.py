from app.models.comment import CommentsModel
from app.db.database import db
from uuid import UUID
from fastapi import HTTPException
from pymongo import DESCENDING


collection = db.get_collection("comments_collection")


async def createComment(comment: CommentsModel):
    try:
        comment_dict = comment.dict(by_alias=True)
        comment_dict["_id"] = str(comment_dict["_id"])
        result = await collection.insert_one(comment_dict)

        if comment_dict["parent_id"]:
            comment_id = comment_dict["parent_id"]
            await updateComment(comment_id, {"hasReplies": True})

        return await getSingleComment(result.inserted_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def getComments(user_id: str):
    try:
        pipeline = [
            {"$match": {"user_id": user_id}},  # Filter by user_id
            {
                "$lookup": {
                    "from": "users_collection",  # Name of the users collection
                    "localField": "user_id",  # The field in comments (user_id)
                    "foreignField": "_id",  # The field in users (user _id)
                    "as": "sendBy",  # Output array name
                }
            },
            {
                "$sort": {"created_at": DESCENDING}
            },  # Sort by created_at in descending order
        ]

        return await collection.aggregate(pipeline).to_list(length=100)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        collection.update_one({"_id": comment_id}, {"$set": update_data})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
