import datetime
from typing import Optional

from pydantic import UUID4
from pydantic import BaseModel as BM
from pydantic import Field, validator


class UserCreate(BM):
    company: str
    username: str
    email: str
    password: str


class UserOut(BM):
    user_id: int
    username: str

    class Config:
        orm_mode = True


class Token(BM):
    access_token: UUID4 = Field(...)
    expires: datetime.datetime
    user_id: int
    token_type: Optional[str] = "bearer"

    class Config:
        orm_mode = True

    @validator("access_token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class TokenOut(BM):
    access_token: str
    token_type: str
    # + 
    client_id: int

    class Config:
        orm_mode = True
