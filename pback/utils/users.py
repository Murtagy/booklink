import hashlib
import random
import string
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore
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


def jwtfy(token: models.Token):
    return jwt.encode({"sub": str(token.token_id)}, SECRET_KEY, algorithm=ALGORITHM)


def unjwttfy_token_id(token: Optional[str]) -> Optional[str]:
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")
