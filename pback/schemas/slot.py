import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel as BM


class CreateSlot(BM):
    name: str
    slot_type: Union[Literal["busy"], Literal["working"], Literal["visit"]]
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime


class UpdateSlot(BM):
    # slot_id: int
    name: Optional[str]
    from_datetime: Optional[datetime.datetime]
    to_datetime: Optional[datetime.datetime]


class Slot(BM):
    slot_id: int

    class Config:
        orm_mode = True
