import datetime
import random
from typing import Literal

from fastapi.exceptions import HTTPException
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

from .availability import Availability, TimeSlotType, _get_client_availability


class CreateSlot(BM):
    name: str
    slot_type: TimeSlotType
    client_id: int
    worker_id: int | None
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
    name: str | None
    from_datetime: datetime.datetime | None
    to_datetime: datetime.datetime | None


class Slot(BM):
    slot_id: int

    class Config:
        orm_mode = True


class WeeklySlot(BM):
    slot_id: int
    mo: list[list[datetime.time]] | None
    tu: list[list[datetime.time]] | None
    we: list[list[datetime.time]] | None
    th: list[list[datetime.time]] | None
    fr: list[list[datetime.time]] | None
    st: list[list[datetime.time]] | None
    su: list[list[datetime.time]] | None

    class Config:
        orm_mode = True


class CreateWeeklySlot(BM):
    mo: list[tuple[str, str]] | None
    tu: list[tuple[str, str]] | None
    we: list[tuple[str, str]] | None
    th: list[tuple[str, str]] | None
    fr: list[tuple[str, str]] | None
    st: list[tuple[str, str]] | None
    su: list[tuple[str, str]] | None
