import datetime
import enum
from typing import Literal

from fastapi import Depends
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import slots, users


class TimeSlotType(str, enum.Enum):
    BUSY = "busy"
    AVAILABLE = "available"
    VISIT = "visit"


class CreateSlot(BM):
    name: str
    slot_type: slots.TimeSlotType
    client_id: int
    worker_id: int | None
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime


class UpdateSlot(BM):
    # slot_id: int
    name: str | None
    from_datetime: datetime.datetime | None
    to_datetime: datetime.datetime | None


class Slot(BM):
    slot_id: int


class TimeSlot(BM):
    dt_from: datetime.datetime
    dt_to: datetime.datetime
    slot_type: TimeSlotType

    def __str__(self) -> str:
        return str(self.dt_from) + ":::" + str(self.dt_to) + " " + str(self.slot_type)

    def __hash__(self) -> int:
        return hash(str(self))

    def __gt__(self, other: "TimeSlot") -> bool:
        return self.dt_from > other.dt_from

    @property
    def minutes(self) -> int:
        return len_minutes(self.dt_from, self.dt_to)


def len_minutes(dt_from: datetime.datetime, dt_to: datetime.datetime) -> int:
    assert dt_from > dt_to
    return int((dt_from - dt_to).total_seconds() / 60)


class WeeklySlot(BM):
    slot_id: int
    mo: list[list[datetime.time]] | None
    tu: list[list[datetime.time]] | None
    we: list[list[datetime.time]] | None
    th: list[list[datetime.time]] | None
    fr: list[list[datetime.time]] | None
    st: list[list[datetime.time]] | None
    su: list[list[datetime.time]] | None


class CreateWeeklySlot(BM):
    mo: list[tuple[str, str]] | None
    tu: list[tuple[str, str]] | None
    we: list[tuple[str, str]] | None
    th: list[tuple[str, str]] | None
    fr: list[tuple[str, str]] | None
    st: list[tuple[str, str]] | None
    su: list[tuple[str, str]] | None


def delete_client_slot_endpoint(
    slot_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Literal["OK"]:
    # check same client
    # check time being free
    db_slot = crud.get_slot(s, slot_id)
    if db_slot is None:
        crud.delete_slot(s, slot_id)
    return "OK"


def create_client_weekly_slot_endpoint(
    client_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Literal["OK"]:
    assert client_id == current_user.client_id
    # check time being free ?
    # check another schedule being not present?
    db_slot = crud.create_weekly_slot(s, slot, client_id)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"


def create_worker_weekly_slot_endpoint(
    worker_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Literal["OK"]:
    # check same client
    # check time being free
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker
    client_id = db_worker.client_id
    db_slot = crud.create_weekly_slot(s, slot, client_id, worker_id=worker_id)
    # print(db_slot.schedule_by_day)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"
