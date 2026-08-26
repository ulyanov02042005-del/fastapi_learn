from dotenv import dotenv_values
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from .schemas import UserInDB
from .database import fake_users_db
from datetime import datetime, timedelta, timezone


config = dotenv_values(".env")
SECRET_KEY = config.get("SECRET_KEY")
ALGORITHM = config.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 45)

password_hash = PasswordHash.recommended()
dummy_hash = password_hash.hash("dummy")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    return password_hash.hash(password=password)

def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password=password, hash=hashed)

def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)
    return None

def authenticate_user(db, username: str, password:str):
    user = get_user(db, username)
    if not user:
        verify_password(password=password, hashed=dummy_hash)
        return False
    if not verify_password(password=password, hashed=user.hashed_password):
        return False
    return user


def token_create(data: dict, expires_delta: timedelta | None = None):
    user = data.copy()
    if expires_delta:
        expiration = datetime.now(timezone.utc) + expires_delta
    else:
        expiration = datetime.now(timezone.utc) + timedelta(minutes=30)
    user.update({"exp": expiration})
    token = jwt.encode(user, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_jwt.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def get_admin_user(user: Annotated[UserInDB, Depends(get_current_user)]):
    if user.role == "admin":
        return user
    raise NotEnoughPermissionsError(user)