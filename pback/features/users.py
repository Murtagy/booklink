import datetime
import hashlib
import random
import string
from typing import Literal, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # type: ignore
from pydantic import UUID4
from pydantic import BaseModel as BM
from pydantic import Field, validator
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions as exceptions
import crud
import db
import models

oauth = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

SECRET_KEY = "12325e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def make_salt():
    return "".join(random.choice(string.ascii_letters) for _ in range(12))


def hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or make_salt()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${enc.hex()}"


def validate_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed_password


class UserCreate(BM):
    company: str
    username: str
    email: str
    password: str


class UserOut(BM):
    client_id: int
    user_id: int
    username: str


class Token(BM):
    access_token: UUID4 = Field(...)
    expires: datetime.datetime
    user_id: int
    token_type: Optional[str] = "bearer"

    @validator("access_token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class TokenOut(BM):
    access_token: str
    token_type: str
    # +
    client_id: int


async def get_current_user_or_none(
    token: Optional[str] = Depends(oauth), s: Session = Depends(db.get_session)
) -> Optional[models.User]:
    if token:
        return await get_current_user(token, s)
    return None


async def get_current_user(
    token: Optional[str] = Depends(oauth), s: Session = Depends(db.get_session)
) -> models.User:
    try:
        token_id = unjwttfy_token_id(token)
        if token_id is None:
            raise exceptions.BadToken
    except JWTError:
        raise exceptions.BadToken
    user = crud.get_user_by_token_id(s, token_id=token_id)
    if user is None:
        raise exceptions.BadToken
    return user


def jwtfy(token: models.Token) -> str:
    return jwt.encode({"sub": str(token.token_id)}, SECRET_KEY, algorithm=ALGORITHM)


def unjwttfy_token_id(token: Optional[str]) -> Optional[str]:
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")


async def create_user_endpoint(
    user: UserCreate, s: Session = Depends(db.get_session)
) -> dict[str, str | int]:
    # print(user)
    # return {"access_token": 'asda', "token_type": "bearer"}

    db_user = crud.get_user_by_email(s, user.email)
    if db_user:
        raise exceptions.EmailExists
    db_user = crud.get_user_by_username(s, user.username)
    if db_user:
        raise exceptions.UsernameExists
    db_client = crud.create_client(s, user.company)
    db_user = crud.create_user(s, user, db_client.client_id)
    # TODO add to client created_by user
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt = jwtfy(access_token)
    return {
        "access_token": jwt,
        "token_type": "bearer",
        "client_id": db_client.client_id,
    }


async def read_users_me_endpoint(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    return current_user


async def read_users_me2_endpoint(
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> Optional[models.User]:
    return current_user


async def login_for_access_token_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(),
    s: Session = Depends(db.get_session),
) -> dict[Literal["access_token", "token_type"], str]:
    db_user = crud.get_user_by_username(s, form_data.username)
    if not db_user:
        raise exceptions.BadCreds
    hashed_password = db_user.hashed_password
    if not (validated := validate_password(form_data.password, hashed_password)):
        raise exceptions.BadCreds
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt_token = jwtfy(access_token)
    return {"access_token": jwt_token, "token_type": "bearer"}
