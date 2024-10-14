from app.models.comment import CommentsModel
from app.db.database import db
from uuid import UUID
from fastapi import HTTPException


collection = db.get_collection("comments_collection")


async def createComment(comment: CommentsModel):
    try:
        comment_dict = comment.dict(by_alias=True)
        result = await collection.insert_one(comment_dict)

        if comment_dict["parent_id"]:
            comment_id = UUID(comment_dict["parent_id"])
            await updateComment(comment_id, {"hasReplies": True})

        return await collection.find_one({"_id": result.inserted_id})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def getComments(user_id: str):
    try:
        return await collection.find({"user_id": user_id}).to_list(length=100)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


async def updateComment(comment_id: str, update_data: dict):
    try:
        collection.update_one({"_id": comment_id}, {"$set": update_data})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
