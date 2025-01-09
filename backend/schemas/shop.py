from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
from fastapi import UploadFile,File
from typing import Annotated, List, Union
from enum import Enum

class ChoiceNameEnum(str, Enum):
    choice1 = "Nike Dunk Retro"
    choice2 = "Nike Air Jordan 1"
    choice3 = "Nike Air Max Plus"
    choice4 = "Nike Dunk x Travis Scott"


class ChoiceTypeEnum(str, Enum):
    choice1 = "Shoes"


class GenderEnum(str, Enum):
    choice1 = "Men's"
    choice2 = "Woman's"
    choice3 = "Men's / Woman's"
    

class DiscountEnum(str, Enum):
    choice1 = "Best Seller"
    choice2 = "New Arrival"
    choice3 = "Sale"
    choice4 = "Sustainable Materials"


class SizeEnum(str, Enum):
    choice1 = "36"
    choice2 = "37"
    choice3 = "38"
    choice4 = "39"
    choice5 = "40"
    choice6 = "41"
    choice7 = "42"
    choice8 = "43"
    choice9 = "44"


class ShopModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str = Field(..., max_length=100, description="Name of the clothes")
    gender: GenderEnum = Field(None, max_length=1000, description="Gender of the clothes")
    type_of_clothes: ChoiceTypeEnum = Field(..., description="Type of the clothes")
    name_of_clothes: ChoiceNameEnum = Field(..., description="Name of the clothes")
    discount: DiscountEnum = Field(None, max_length=100, description="Discount of the clothes")
    price: float = Field(..., ge=0, description="Price of the clothes")
    created_at: datetime = Field(default_factory=datetime.now, description="Date of the creation")
    sizes: Optional[List[SizeEnum]] = Field(None, description="Available sizes of the clothes")
    photo: Annotated[UploadFile, File(...)]
    photo_hover: Annotated[UploadFile, File(...)]
    add_photos: List[UploadFile] = None
    variable: Optional[Annotated[UploadFile, File(None)]] = None
    description: Optional[str] = Field(..., max_length=350, description="Description of clothes")
    styles: Optional[str] = Field(None)
    model: str = None
    
    @field_validator("created_at")
    @classmethod
    def check_date(cls, value):
        if value.timestamp() > datetime.now().timestamp():
            raise ValueError("Date cannot be in the future")
        return value
    
    @field_validator("sizes", mode="before")
    @classmethod
    def normalize_sizer(cls, value):
        if value:
            return value[0].split(",")
        return value