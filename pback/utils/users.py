import hashlib
import random
import string
from typing import Optional

from fastapi.security import OAuth2PasswordBearer

oauth = OAuth2PasswordBearer(tokenUrl="token")


def make_salt():
    return "".join(random.choice(string.ascii_letters) for _ in range(12))


def hash_password(password: str, salt: Optional[str] = None) -> str:
    salt = salt or make_salt()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${enc.hex()}"


def validate_password(password: str, hashed_password: str) -> bool:
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed
