from ..db.models import User
from ..db import Session
from ..schemas.token import TokenData

from os import getenv
from typing import Annotated
from datetime import timedelta, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from bcrypt import checkpw
import jwt



load_dotenv()

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticate_user(
    username: str,
    password: str
):
    async with Session() as session:
        user = await session.scalar(select(User).where(User.name == username))
        if not user:
            return False
        print(password, user.password)
        if not await checkpw(password, user.password):
            return False
        return user


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)]
):
    async with Session() as session:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)

        except Exception:
            raise credentials_exception
        print(token_data.username)
        user = await session.scalar(select(User).where(User.name == token_data.username))
        if user is None:
            raise credentials_exception
        return user