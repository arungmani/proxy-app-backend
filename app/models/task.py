from pydantic import BaseModel, Field
from bson import ObjectId, Binary, UuidRepresentation
from typing import Optional
from datetime import datetime
from typing import List


import uuid

class AssigneeModel(BaseModel):
    first_name: str
    last_name: str
    _id: str

class TaskModel(BaseModel):
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    due_date: Optional[datetime] = Field(None)
    country: Optional[str] = Field(None)
    state: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)
    volunteer_id: Optional[str] = Field(None)  # Storing volunteer_id as UUID
    assignees: Optional[List[AssigneeModel]] = []
    created_by: Optional[str] = Field(None)  # Storing created_by as UUID
    created_on: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp())
    )
    confirmed_on: Optional[int] = Field(None)
    completed_on: Optional[int] = Field(None)
    remarks: Optional[str] = Field(None)
    is_completed: bool = Field(default=False)
    status: Optional[str] = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "title": "Community Cleanup",
                "description": "Organize a community cleanup event",
                "due_date": "2024-09-15T18:00:00",
                "priority": "High",
                "volunteer_id": "64f5a7b2d8c7c3d3f7a0b3f1",
                "created_by": "64f5a7b2d8c7c3d3f7a0b3f1",
                "created_on": 1725123456,  # Example timestamp
                "confirmed_on": 1726200000,  # Example timestamp
                "completed_on": 1726785600,  # Example timestamp
                "remarks": "Task completed successfully.",
                "is_completed": False,
            }
        }
