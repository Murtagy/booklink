import datetime
from typing import Optional

from pydantic import UUID4
from pydantic import BaseModel as BM
from pydantic import Field, validator


class UserCreate(BM):
    user_name: str
    email: str
    password: str


class UserOut(BM):
    user_id: int
    user_name: str

    class Config:
        orm_mode = True


class Token(BM):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime.datetime
    token_type: Optional[str] = "bearer"

    class Config:
        orm_mode = True

    @validator("token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class TokenOut(UserOut):
    token: Token
