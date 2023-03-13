import datetime
import enum
from typing import Any, Literal, Optional

from fastapi import Depends, Query
from pydantic import BaseModel as BM
from pydantic import validator
from sqlalchemy.orm import Session  # type: ignore

from server.models import SlotType

from .. import app_exceptions, crud, db, models
from ..dates import localize
from . import availability, customers, services, users, workers


class InServiceToVisit(BM):
    service_id: int


class TimeSlotType(str, enum.Enum):
    BUSY = "busy"
    AVAILABLE = "available"
    VISIT = "visit"


class CreateSlot(BM):
    slot_type: TimeSlotType
    worker_id: int | None
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime
    has_notification = False
    status = "submitted"
    customer_info: customers.CustomerInfoIn | None = None
    services: list[InServiceToVisit] = []

    @validator("to_datetime", "from_datetime")
    def localize(cls, v: datetime.datetime):
        return localize(v)

    @validator("to_datetime", always=True)
    def date_to_check(cls, v: datetime.date, values: dict[str, Any]):
        if v < values["from_datetime"]:
            raise ValueError("to should be greater than from")
        delta: datetime.timedelta = v - values["from_datetime"]
        if delta > datetime.timedelta(days=1):
            raise ValueError("range is too big")
        return v

    @classmethod
    def Available(
        cls,
        *,
        worker_id: int | None,
        from_datetime: datetime.datetime,
        to_datetime: datetime.datetime,
    ):
        return cls(
            slot_type=TimeSlotType.AVAILABLE,
            worker_id=worker_id,
            from_datetime=from_datetime,
            to_datetime=to_datetime,
        )


class UpdateSlot(BM):
    # slot_id: int
    from_datetime: datetime.datetime | None
    to_datetime: datetime.datetime | None


class OutSlot(BM):
    slot_id: int
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime
    slot_type: str  # busy/visit/available
    worker_id: int | None

    class Config:
        orm_mode = True


class TimeSlot(BM):
    """Both in and Out"""

    dt_from: datetime.datetime
    dt_to: datetime.datetime
    slot_type: TimeSlotType

    @validator("dt_from", "dt_to")
    def localize(cls, v):
        return localize(v)

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


def delete_client_slot(
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


class OutVisit(BM):
    email: str | None
    has_notification: bool
    phone: str | None
    status: str
    slot_id: int
    worker_id: int | None
    created_at: datetime.datetime
    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    class Config:
        orm_mode = True


class OutVisitExtended(BM):
    services: list[services.OutService]
    slot: OutSlot
    visit: OutVisit
    worker: workers.OutWorker | None


class Received(BM):
    msg: Literal["OK"] = "OK"


class InVisit(BM):
    client_id: int
    from_dt: datetime.datetime
    services: list[InServiceToVisit]
    remind_me: bool
    version: Literal[1] = 1
    worker_id: str | None

    # change to customer info?
    phone: str
    email: str
    first_name: str
    last_name: str

    @validator("from_dt")
    def localize(cls, v):
        return localize(v)


class VisitDay(BM):
    date: datetime.date
    visits_n: int
    visits: list[OutVisit]


class VisitsByDays(BM):
    days: list[VisitDay]


class VisitsByDaysRQ(BM):
    date_from: datetime.date
    date_to: datetime.date

    @validator("date_to")
    def date_to_check(cls, v: datetime.date, values: dict[str, Any]):
        if v < values["date_from"]:
            raise ValueError("to should be greater than from")
        delta: datetime.timedelta = v - values["date_from"]
        if delta > datetime.timedelta(days=7):
            raise ValueError("range is too big")
        return v


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
) -> list[models.Slot]:
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


def get_visits_days(
    rq: VisitsByDaysRQ,
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> VisitsByDays:
    client_id = current_user.client_id

    visits_by_days: dict[datetime.date, list[models.Slot]] = {}
    for d in range((rq.date_to - rq.date_from).days + 1):
        date = rq.date_from + datetime.timedelta(days=d)
        visits_by_days[date] = []

    visits = crud.get_visits(s, client_id, worker_id=worker_id, _from=rq.date_from, _to=rq.date_to)
    for visit in visits:
        visits_by_days[visit.from_datetime.date()].append(visit)
    days = []
    for date, visits in visits_by_days.items():
        days.append(
            VisitDay(date=date, visits_n=len(visits), visits=[OutVisit.from_orm(v) for v in visits])
        )
    return VisitsByDays(days=days)


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
) -> models.Slot:
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise app_exceptions.VisitNotFound
    return visit


def create_slot_with_check(
    slot: CreateSlot,
    force: bool = Query(False),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> OutSlot:
    if slot.slot_type == TimeSlotType.VISIT and not force:
        # in case slot is a visit - check for collision
        slot = availability.visit_pick_worker_or_throw(
            s, slot, current_user.client_id, exc=app_exceptions.SlotNotAvailable
        )
    # others we let to duplicate

    if slot.worker_id:
        workers.assure_worker_and_owner(s, current_user, slot.worker_id)

    db_slot = crud.create_slot(s, slot, current_user.client_id)
    return OutSlot.from_orm(db_slot)


def create_slot(slot: CreateSlot, s: Session, client_id: int) -> OutSlot:
    db_slot = crud.create_slot(s, slot, client_id)
    return OutSlot.from_orm(db_slot)


def create_slots(
    client_id: int,
    slots: list[CreateSlot],
    s: Session,
) -> None:
    """only available slots"""
    for slot in slots:
        if slot.slot_type != SlotType.AVAILABLE:
            raise ValueError("wrong slot type")
    crud.create_slots(s, slots, client_id)


def public_book_visit(
    visit: InVisit,
    s: Session = Depends(db.get_session),
) -> OutVisitExtended:
    if visit.from_dt < datetime.datetime.now():
        raise app_exceptions.SlotNotAvailable

    service_ids = [s.service_id for s in visit.services]
    visit_services = services.get_services_by_ids(service_ids, s=s)
    assert len(visit_services) > 0
    visit_len_minutes: int = sum([service.minutes for service in visit_services])

    potential_slot = CreateSlot(
        slot_type=TimeSlotType.VISIT,
        worker_id=visit.worker_id,
        from_datetime=visit.from_dt,
        to_datetime=visit.from_dt + datetime.timedelta(minutes=visit_len_minutes),
    )
    potential_slot = availability.visit_pick_worker_or_throw(
        s, potential_slot, visit.client_id, exc=app_exceptions.SlotNotAvailable
    )
    slot = create_slot(potential_slot, s, visit.client_id)

    db_visit = crud.create_customer_visit(
        s,
        visit,
        to_dt=potential_slot.to_datetime,
        worker_id=slot.worker_id,
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


def delete_available_slots(
    dates: list[datetime.date],
    worker_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> None:
    crud.delete_available_slots(s, current_user.client_id, worker_id, dates)
