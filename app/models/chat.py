from pydantic import BaseModel, Field
from bson import ObjectId, Binary, UuidRepresentation
from typing import Optional
from datetime import datetime
import uuid


class chat(BaseModel):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, alias="_id")
    task_owner_id:Optional[str] = Field(None)
    task_volunteer_id:Optional[str] = Field(None)
    message:Optional[str]=Field(None)
    sender:Optional[str]=Field(None)
    created_on: Optional[int] = Field(default_factory=lambda: int(datetime.now().timestamp()))
  

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "message": "Community Cleanup",
                "sender":"taskowner/taskassigner",
                "task_owner_id":"64f5a7b2d8c7c3d3f7a0b3f1",
                "volunteer_id": "64f5a7b2d8c7c3d3f7a0b3f1",
                "created_by": "64f5a7b2d8c7c3d3f7a0b3f1",
                "created_on": 1725123456,  # Example timestamp
            
            }
        }

