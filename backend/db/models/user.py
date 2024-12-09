from .. import Base
from sqlalchemy.orm import Mapped,mapped_column,validates
from bcrypt import hashpw, gensalt

class User(Base):
    __tablename__ = "users"
    
    username:Mapped[str] = mapped_column(nullable=False,unique=True)
    password:Mapped[str] = mapped_column(nullable=False)\
    
    @validates("password")
    def validate_password(self,key,value):
        hashed_password = hashpw(value.encode("utf-8"), gensalt())
        return hashed_password.decode("utf-8")