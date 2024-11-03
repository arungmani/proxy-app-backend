from pydantic import BaseModel, Field
from bson import ObjectId, Binary, UuidRepresentation
from typing import Optional, Dict
from datetime import datetime
import uuid


class CommentsModel(BaseModel):
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
    task_id: Optional[str] = Field(None)
    sender: Optional[Dict[str, Optional[str]]] = Field(
        None, description="Information about the user who sent the comment"
    )
    comment: Optional[str] = Field(None)
    parent_id: Optional[str] = Field(None)
    hasReplies: Optional[bool] = Field(
        default=False
    )  # using the isReplies field to indicate that a message has replies,
    created_at: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp())
    )

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "comment": "Community Cleanup",
                "task_id": "869931d8-c720-4c37-ade4-1eedaf5b0033",
                "sender": {"user_id": "64f5a7b2d8c7c3d3f7a0b3f1","first_name":"Yesudas"},
                "parent_id": "64f5a7b2d8c7c3d3f7a0b3f1",
                "created_at": 1725123456,  # Example timestamp
            }
        }
