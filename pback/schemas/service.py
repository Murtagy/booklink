from typing import Optional

from pydantic import BaseModel as BM


class CreateService(BM):
    name: str
    price: Optional[float]
    price_lower_bound: Optional[float]
    price_higher_bound: Optional[float]
    seconds: int
    description: Optional[str]


class OutService(BM):
    service_id: int
    name: str
    price: Optional[float]
    price_lower_bound: Optional[float]
    price_higher_bound: Optional[float]
    seconds: int
    description: str

    class Config:
        orm_mode = True
