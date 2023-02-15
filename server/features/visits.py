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
from features import availability, services, slots, users, workers
from features.slots import TimeSlotType


class InServiceToVisit(BM):
    service_id: int


class OutVisit(BM):
    version: Literal[1] = 1

    email: str | None
    has_notification: bool
    phone: str | None
    status: str
    visit_id: int
    worker_id: int | None

    class Config:
        orm_mode = True


class OutVisitExtended(BM):
    services: list[services.OutService]
    slot: slots.OutSlot
    visit: OutVisit
    worker: workers.OutWorker | None


class Received(BM):
    msg: Literal["OK"] = "OK"


class InVisit(BM):
    client_id: int
    from_dt: datetime.datetime
    # to_dt: datetime.datetime
    first_name: str
    last_name: str
    email: str
    services: List[InServiceToVisit]
    phone: str
    remind_me: bool
    version: Literal[1] = 1
    worker_id: str | None


# class VisitStatus(SEnum):
#     SUMBITTED = 'submitted'  # -> R/A
#     REJECTED = 'rejected'
#     APPROVED = 'approved'  # -> C
#     CANCELLED = 'cancelled'
#     # MISSED = 'missed'
#     # FINISHED = 'finished'


def get_visits(
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> list[models.Visit]:
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


def update_visit(
    visit_id: str,
    visit: InVisit,
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> None:
    return None


def get_visit(
    visit_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Visit:
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise app_exceptions.VisitNotFound
    return visit


def create_slot(
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


def create_visit_slot(
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


def public_book_visit(
    visit: InVisit,
    s: Session = Depends(db.get_session),
    # TODO: visitor
) -> OutVisitExtended:
    if visit.from_dt < datetime.datetime.now():
        raise app_exceptions.SlotNotAvailable

    service_ids = [s.service_id for s in visit.services]
    visit_services = services.get_services_by_ids(service_ids, s=s)
    assert len(visit_services) > 0
    visit_len_seconds: int = sum([service.seconds for service in visit_services])

    potential_slot = slots.CreateSlot(
        name=f"Визит в {visit.from_dt}",
        slot_type=slots.TimeSlotType.VISIT,
        client_id=visit.client_id,
        worker_id=visit.worker_id,
        from_datetime=visit.from_dt,
        to_datetime=visit.from_dt + datetime.timedelta(seconds=visit_len_seconds),
    )
    potential_slot = availability.visit_pick_worker_and_check(
        s, potential_slot, exc=app_exceptions.SlotNotAvailable
    )
    slot = slots.create_slot(s, potential_slot)

    db_visit = crud.create_customer_visit(
        s,
        visit,
        slot_id=slot.slot_id,
        worker_id=slot.worker_id,
        customer_id=None,
    )
    out_visit = OutVisit.from_orm(db_visit)

    worker = None
    if db_visit.worker_id:
        worker = workers.get_worker_by_id(db_visit.worker_id, s=s)

    return OutVisitExtended(
        slot=slot,
        services=visit_services,
        visit=out_visit,
        worker=worker,
    )
