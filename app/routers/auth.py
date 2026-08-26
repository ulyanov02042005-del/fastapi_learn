from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..database import fake_users_db
from ..dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    hash_password,
    token_create,
)
from ..schemas import Token, User, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", status_code=201)
async def register(user: UserCreate) -> User:
    user_db_data = user.model_dump(exclude_unset=True)
    raw_password = user_db_data.pop("password")
    user_db_data["hashed_password"]=hash_password(raw_password)
    fake_users_db[user.username] = user_db_data
    return user_db_data

@router.post("/login")
async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_logged = authenticate_user(fake_users_db, username=user.username, password=user.password)
    if not user_logged:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expiration_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_create(data={"sub": user.username}, expires_delta=expiration_time)
    return Token(access_token=access_token, token_type="bearer")
    