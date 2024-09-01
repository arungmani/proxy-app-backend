from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from app.models.item import PyObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: int = Field(...)
    user_type: str = Field(...)
    created_on: Optional[int] = Field(default_factory=lambda: int(datetime.utcnow().timestamp()))

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": 1234567890,
                "user_type": "admin",
                "created_on": "2024-08-31T12:34:56"
            }
        }