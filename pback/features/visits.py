""" Visits sit a top of slots. So they use both slots and availability features."""

import datetime
from typing import List, Literal, Optional

from fastapi import Depends
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions
import crud
import db
import models
from features import availability, slots, users
from features.slots import TimeSlotType


class InServiceToVisit(BM):
    service_id: int


class OutVisit(BM):
    version: Literal[1] = 1
    phone: Optional[str]
    # from_dt: datetime.datetime
    # to_dt: datetime.datetime


    @classmethod
    def Example(cls) -> "OutVisit":
        return cls(
            phone="375291231123",
        )


class Received(BM):
    msg: Literal["OK"] = "OK"


class InVisit(BM):
    client_id: int
    from_dt: datetime.datetime
    # to_dt: datetime.datetime
    email: str
    services: List[InServiceToVisit]
    phone: str
    remind_me: bool
    version: Literal[1] = 1
    worker_id: Optional[int]


# class VisitStatus(SEnum):
#     SUMBITTED = 'submitted'  # -> R/A
#     REJECTED = 'rejected'
#     APPROVED = 'approved'  # -> C
#     CANCELLED = 'cancelled'
#     # MISSED = 'missed'
#     # FINISHED = 'finished'


def get_visits_endpoint(
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> list[models.Visit]:
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


def update_visit_endpoint(
    visit_id: str,
    visit: InVisit,
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> None:
    return None


def get_visit_endpoint(
    visit_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Visit:
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise app_exceptions.VisitNotFound
    return visit


def create_slot_endpoint(
    slot: slots.CreateSlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Slot:
    if slot.slot_type == TimeSlotType.VISIT:
        # in case slot is a visit - check for collision
        slot = availability.visit_pick_worker_and_check(
            s, slot, exc=app_exceptions.SlotNotAvailable
        )
    # others we let to duplicate
    db_slot = crud.create_slot(s, slot)
    return db_slot


# this endpoint use ?
# def create_visit_endpoint(
#     visit: InVisit,
#     s: Session = Depends(db.get_session),
#     current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
# ) -> models.Visit:
#     db_visit = crud.create_visit(s, visit)
#     return db_visit


def create_visit_slot_endpoint(
    slot: slots.CreateSlot,
    s: Session = Depends(db.get_session),
) -> models.Visit:
    if slot.slot_type not in [TimeSlotType.VISIT]:
        raise app_exceptions.SlotType

    slot = availability.visit_pick_worker_and_check(s, slot, exc=app_exceptions.SlotNotAvailable)
    db_slot = crud.create_slot(s, slot)
    db_visit = crud.create_visit(
        s,
        client_id=db_slot.client_id,
        slot_id=db_slot.slot_id,
        worker_id=db_slot.worker_id,
    )
    return db_visit


def public_book_visit_endpoint(
    visit: InVisit,
    s: Session = Depends(db.get_session),
    # TODO: visitor
) -> models.Visit:
    if visit.from_dt < datetime.datetime.now():
        raise app_exceptions.SlotNotAvailable

    services = crud.get_services_by_ids(s, [s.service_id for s in visit.services])
    assert len(services) > 0
    visit_len_seconds: int = sum([service.seconds for service in services])

    slot = slots.CreateSlot(
        name=f"Визит в {visit.from_dt}",
        slot_type=slots.TimeSlotType.VISIT,
        client_id=visit.client_id,
        worker_id=visit.worker_id,
        from_datetime=visit.from_dt,
        to_datetime=visit.from_dt + datetime.timedelta(seconds=visit_len_seconds),
    )
    slot = availability.visit_pick_worker_and_check(s, slot, exc=app_exceptions.SlotNotAvailable)

    db_slot = crud.create_slot(s, slot)

    db_visit = crud.create_customer_visit(
        s,
        visit,
        slot_id=db_slot.slot_id,
        worker_id=db_slot.worker_id,
        customer_id=None,
    )
    return db_visit
