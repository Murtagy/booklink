from pydantic import BaseModel as BM


class UserCreate:
    user_name: str
    email: str
    password: str


class UserOut:
    user_id: int
    user_name: str

    class Config:
        orm_mode = True
