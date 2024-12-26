from fastapi import APIRouter, HTTPException, status, Depends, Query
from uuid import UUID
from typing import List
from app.common.helper import verify_jwt
from app.models.comment import CommentsModel
from app.services.comment_service import createComment
from app.services.comment_service import getComments
from typing import Optional
from app.services.comment_service import updateComment
from app.services.comment_service import deleteSingleComment


router = APIRouter(tags=["comment"], responses={404: {"description": "Not found"}})

# Create Task


@router.post("/comment/add")
async def create_comment(
    data: CommentsModel,
    user: dict = Depends(verify_jwt),
):
    try:
        print("The comment data is", data.sender["user_id"])
        result = await createComment(data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/comment/list/{task_id}")
async def list_user_comments(
    task_id: str,
    user_id: dict = Depends(verify_jwt),
    parent_id: Optional[str] = Query(None),
):
    try:
        print("THE PARENT ID IS", parent_id)

        comments = await getComments(
            task_id,
            parent_id,
        )
        return comments
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/comment/update/{comment_id}")
async def update_comment(comment_id: str, data: CommentsModel):
    try:
        result = await updateComment(comment_id, data)
        print("THE UPDATED DATA IS", result)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred when update the comment",
        )


@router.delete("/comment/delete/{comment_id}")
async def delete_comment(comment_id: str):
    try:
        result = await deleteSingleComment(comment_id)
        print("the deleted data", result)
        if result:
            return "Comment deleted successfully"
        else:
            return "Comment not found"
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred when update the comment",
        )
