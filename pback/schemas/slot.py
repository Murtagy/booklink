import datetime
import random
from typing import List, Literal, Optional, Tuple, Union

from fastapi.exceptions import HTTPException
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

from .availability import Availability, _get_client_availability


class CreateSlot(BM):
    name: str
    slot_type: Union[Literal["busy"], Literal["available"], Literal["visit"]]
    client_id: int
    worker_id: Optional[int]
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    async def visit_pick_worker_and_check(
        self, s: Session, *, exc: HTTPException
    ) -> "CreateSlot":
        slot = self
        _worker_id = slot.worker_id
        if _worker_id:
            worker_id = _worker_id
            av = await Availability.GetWorkerAV(s, worker_id)
            if not av.CheckSlot(slot):
                raise exc

        else:
            client_av = await _get_client_availability(slot.client_id, None, s)
            workers_av = [
                worker_id for (worker_id, av) in client_av.items() if av.CheckSlot(slot)
            ]
            if len(workers_av) == 0:
                raise exc

            worker_id = random.choice(workers_av)
            av = await Availability.GetWorkerAV(s, worker_id)
            assert av.CheckSlot(slot)
            slot.worker_id = worker_id
        return slot


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
