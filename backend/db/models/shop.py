from .. import Base
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime

class Shop(Base):

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=False)
    price:Mapped[float] = mapped_column(nullable=True)
    created_at:Mapped[datetime] = mapped_column(nullable=False)
    photo:Mapped[str] = mapped_column(nullable=False)