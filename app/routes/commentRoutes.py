from fastapi import APIRouter, HTTPException, status, Depends, Query
from uuid import UUID
from typing import List
from app.common.helper import verify_jwt
from app.models.comment import CommentsModel
from app.services.commentService import createComment
from app.services.commentService import getComments

router = APIRouter(tags=["comment"], responses={404: {"description": "Not found"}})

# Create Task


@router.post("/comment/create", response_model=CommentsModel)
async def create_comment(
    data: CommentsModel,
    user: dict = Depends(verify_jwt),
):
    try:
        data.user_id = user  # Assuming 'id' is a part of the JWT payload
        print(data)
        registered_task = await createComment(data)
        return registered_task
    except ValueError as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/comments/list")
async def list_user_comments(
    user_id: dict = Depends(verify_jwt),
):
    try:
        comments = await getComments(user_id)
        return comments
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
