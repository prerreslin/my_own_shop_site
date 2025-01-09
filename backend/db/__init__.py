from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase,mapped_column,Mapped


engine = create_engine("sqlite:///test.db",echo=True)
Session = sessionmaker(bind=engine)


class classproperty:
    def __init__(self, method):
        self.method = method
    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        return self.method(cls)


class Base(DeclarativeBase):

    @classproperty
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"



from . import models

def up():
    Base.metadata.create_all(bind=engine)

def down():
    Base.metadata.drop_all(bind=engine)

# down()
up()