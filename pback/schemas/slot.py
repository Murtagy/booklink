import datetime
from typing import List, Literal, Optional, Tuple, Union

from pydantic import BaseModel as BM


class CreateSlot(BM):
    name: str
    slot_type: Union[Literal["busy"], Literal["available"], Literal["visit"]]
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


class WeeklySlot(BM):
    slot_id: int
    mo: Optional[List[List[datetime.time]]]
    tu: Optional[List[List[datetime.time]]]
    we: Optional[List[List[datetime.time]]]
    th: Optional[List[List[datetime.time]]]
    fr: Optional[List[List[datetime.time]]]
    st: Optional[List[List[datetime.time]]]
    su: Optional[List[List[datetime.time]]]

    class Config:
        orm_mode = True


class CreateWeeklySlot(BM):
    mo: Optional[List[Tuple[str, str]]]
    tu: Optional[List[Tuple[str, str]]]
    we: Optional[List[Tuple[str, str]]]
    th: Optional[List[Tuple[str, str]]]
    fr: Optional[List[Tuple[str, str]]]
    st: Optional[List[Tuple[str, str]]]
    su: Optional[List[Tuple[str, str]]]
