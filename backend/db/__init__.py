from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,mapped_column,Mapped


engine = create_engine("sqlite:///test.db",echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)

from . import models

def up():
    Base.metadata.create_all(bind=engine)

def down():
    Base.metadata.drop_all(bind=engine)

up()