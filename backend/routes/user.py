from ..db import Session
from ..db.models import User
from ..app import api_router
from ..schemas import UserModel
from fastapi import HTTPException
from bcrypt import checkpw

@api_router.post("/user/register")
def register(data:UserModel):
    with Session() as session:
        user = session.query(User).where(User.username == data.username).first()

        if user:
            raise HTTPException(409,"User already exists")
        
        user = User(**data.model_dump())

        session.add(user)
        session.commit()
        session.refresh(user)

        return user


@api_router.post("/user/login")
def login(data:UserModel):
    with Session() as session:
        user = session.query(User).where(User.username == data.username).first()
        
        if not user:
            raise HTTPException(404,"User not exists")
        
        if checkpw(data.password.encode("utf-8"),user.password.encode("utf-8")):
            return user
        raise HTTPException(401,"Password is wrong")
        
