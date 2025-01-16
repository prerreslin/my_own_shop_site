from sqlalchemy import Table, Column, Integer, ForeignKey
from .. import Base

user_favourite_table = Table(
    "user_favourites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("shop_id", Integer, ForeignKey("shops.id", ondelete="CASCADE"), primary_key=True),
)