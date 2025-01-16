from .. import Base
from .union import user_favourite_table
from sqlalchemy.orm import Mapped,mapped_column,validates,relationship
from sqlalchemy import ForeignKey
from typing import List
from bcrypt import hashpw, gensalt

class User(Base):
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(nullable=False,unique=True)
    password:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False,unique=True)
    favourites: Mapped[List["Shop"]] = relationship(
        "Shop",
        secondary=user_favourite_table,
        back_populates="users",
    )

    @validates("password")
    def validate_password(self,key,value):
        hashed_password = hashpw(value.encode("utf-8"), gensalt())
        return hashed_password.decode("utf-8")