from .. import Base
from sqlalchemy.orm import Mapped,mapped_column

class Gift_Card(Base):

    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=True)
    price:Mapped[float] = mapped_column(nullable=True)
    photo:Mapped[str] = mapped_column(nullable=False)
    description2:Mapped[str] = mapped_column(nullable=False)