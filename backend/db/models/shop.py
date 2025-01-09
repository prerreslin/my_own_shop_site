from .. import Base
from typing import Dict,List
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.types import JSON
from datetime import datetime

class Shop(Base):

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    type_of_clothes:Mapped[str] = mapped_column(nullable=False)
    name_of_clothes:Mapped[str] = mapped_column(nullable=False)
    discount:Mapped[str] = mapped_column(nullable=True)
    gender:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[float] = mapped_column(nullable=True)
    created_at:Mapped[datetime] = mapped_column(nullable=False)
    sizes:Mapped[Dict] = mapped_column(JSON)
    photo:Mapped[str] = mapped_column(nullable=False)
    photo_hover:Mapped[str] = mapped_column(nullable=False)
    photos:Mapped[List] = mapped_column(JSON)
    variable:Mapped[str] = mapped_column(nullable=True)