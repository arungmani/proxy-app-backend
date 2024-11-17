from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

import uuid


class UserModel(BaseModel):
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    role: Optional[str] = Field(None)
    phone_number: Optional[int] = Field(None)
    user_type: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    created_on: Optional[int] = Field(
        default_factory=lambda: int(datetime.utcnow().timestamp())
    )
    # Ratings as a task creator
    created_task_ratings: Optional[List[float]] = (
        None  # Ratings received for tasks created
    )
    avg_created_task_rating: Optional[float] = None  # Average rating as task creator

    # Ratings as a task assignee
    assigned_task_ratings: Optional[List[float]] = (
        None  # Ratings received for tasks assigned
    )
    avg_assigned_task_rating: Optional[float] = None  # Average rating as task assignee

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@gmail.com",
                "phone_number": 1234567890,
                "user_type": "admin",
                "password": "12333388",
                "created_on": 234234234234,
                "created_task_ratings": [4.5, 5.0],
                "avg_created_task_rating": 4.75,
                "assigned_task_ratings": [4.0],
                "avg_assigned_task_rating": 4.0,
            }
        }
