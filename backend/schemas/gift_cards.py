from pydantic import BaseModel, Field, ConfigDict
from fastapi import UploadFile, File
from typing import Annotated

class GiftCardModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., max_length=30, description="Name of the gift card")
    description: str = Field(..., max_length=30, description="Description of the gift card")
    price: float = Field(..., ge=0, description="Price of the gift card")
    photo: Annotated[UploadFile, File(...)]
    description2: str = Field(..., max_length=350, description="Big description of the gift card")