from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class UserModel(BaseModel):
    id: Optional[str] = Field(default_factory=uuid.uuid4, alias="_id")
    first_name:  Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email:Optional[str]=Field(None)
    role:Optional[str]=Field(None)
    phone_number: Optional[int] = Field(None)
    user_type: Optional[str] = Field(None)
    password:Optional[str]=Field(None)
    created_on: Optional[int] = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = { datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email":'johndoe@gmail.com',
                "phone_number": 1234567890,
                "user_type": "admin",
                "password":'12333388',
                "created_on": 234234234234
            }
        }