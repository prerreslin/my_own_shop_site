from .. import Base
from sqlalchemy.orm import Mapped,mapped_column,validates
from bcrypt import hashpw, gensalt

class User(Base):
    
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(nullable=False,unique=True)
    password:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False,unique=True)


    @validates("password")
    def validate_password(self,key,value):
        hashed_password = hashpw(value.encode("utf-8"), gensalt())
        return hashed_password.decode("utf-8")