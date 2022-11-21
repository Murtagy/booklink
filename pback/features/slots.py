import datetime
import hashlib
import random
import string
from typing import Literal, Optional

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt  # type: ignore
from pydantic import UUID4
from pydantic import BaseModel as BM
from pydantic import Field, validator
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions as exceptions
import crud
import db
import features.users as users
import models
from schemas.availability import Availability, TimeSlotType, _get_client_availability


class CreateSlot(BM):
    name: str
    slot_type: TimeSlotType
    client_id: int
    worker_id: int | None
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    # move to availability?
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


async def delete_client_slot_endpoint(
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


async def create_slot_endpoint(
    slot: CreateSlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> dict[Literal["slot_id"], int]:
    # TODO check against availability
    if slot.slot_type == TimeSlotType.VISIT:
        slot = await slot.visit_pick_worker_and_check(
            s, exc=exceptions.SlotNotAvailable
        )
    # for now I let availiability to duplicate
    db_slot = crud.create_slot(s, slot)
    return {"slot_id": db_slot.slot_id}


async def public_create_slot_endpoint(
    slot: CreateSlot,
    s: Session = Depends(db.get_session),
) -> dict[Literal["slot_id"], int]:
    if slot.slot_type not in [TimeSlotType.VISIT]:
        raise exceptions.SlotType

    slot = await slot.visit_pick_worker_and_check(s, exc=exceptions.SlotNotAvailable)

    db_slot = crud.create_slot(s, slot)
    return {"slot_id": db_slot.slot_id}


async def create_client_weekly_slot_endpoint(
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


async def create_worker_weekly_slot_endpoint(
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
