from ..db import Session
from ..db.models import User
from ..schemas import UserModel,LoginModel
from fastapi import HTTPException, APIRouter
from bcrypt import checkpw


user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/register")
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


@user_router.post("/login")
def login(data:LoginModel):
    with Session() as session:
        user = session.query(User).where(User.email == data.email).first()
        
        if not user:
            raise HTTPException(404,"User not exists")
        
        if checkpw(data.password.encode("utf-8"),user.password.encode("utf-8")):
            return user
        raise HTTPException(401,"Password is wrong")
    

@user_router.get("/get_user_by_email")
def get_user_by_email(email:str):
    with Session() as session:
        user = session.query(User).where(User.email == email).first()
        if not user:
            return {"status":"register"}
        return {"status":"login"}
        

@user_router.get("/get_user_by_id")
def get_user_by_id(user_id:int):
    with Session() as session:
        user = session.query(User).where(User.id == user_id).first()
        if not user:
            raise HTTPException(404,"User not exists")
        return user