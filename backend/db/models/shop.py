from .. import Base
from .union import user_favourite_table
from typing import Dict,List
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.types import JSON
from datetime import datetime

class Shop(Base):

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=True)
    styles:Mapped[str] = mapped_column(nullable=True)
    model:Mapped[str] = mapped_column(nullable=True)
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

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_favourite_table,
        back_populates="favourites",
    )