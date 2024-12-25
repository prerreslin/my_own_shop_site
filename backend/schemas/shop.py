from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
from datetime import datetime
from fastapi import UploadFile,File
from typing import Annotated

class ShopModel(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the clothes")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the clothes")
    price: float = Field(..., ge=0, description="Price of the clothes")
    created_at: datetime = Field(default_factory=datetime.now, description="Date of the creation")
    photo: Annotated[UploadFile, File(...)] = None

    @field_validator("created_at")
    @classmethod
    def check_date(cls, value):
        if value.timestamp() > datetime.now().timestamp():
            raise ValueError("Date cannot be in the future")
        return value