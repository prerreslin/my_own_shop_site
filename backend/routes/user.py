from ..db import Session
from ..db.models import User
from ..app import api_router
from ..schemas import UserModel,LoginModel
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
def login(data:LoginModel):
    with Session() as session:
        user = session.query(User).where(User.email == data.email).first()
        
        if not user:
            raise HTTPException(404,"User not exists")
        
        if checkpw(data.password.encode("utf-8"),user.password.encode("utf-8")):
            return user
        raise HTTPException(401,"Password is wrong")
    

@api_router.get("/user/get_user_by_email")
def get_user_by_email(email:str):
    with Session() as session:
        user = session.query(User).where(User.email == email).first()
        if not user:
            return {"status":"register"}
        return {"status":"login"}
        

@api_router.get("/user/get_user_by_id")
def get_user_by_id(user_id:int):
    with Session() as session:
        user = session.query(User).where(User.id == user_id).first()
        if not user:
            raise HTTPException(404,"User not exists")
        return user
