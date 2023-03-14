import datetime
import math
import random
from typing import Any, Optional

from dateutil.relativedelta import relativedelta
from fastapi import Depends, Path, Query
from fastapi.exceptions import HTTPException
from pydantic import BaseModel as BM
from pydantic import validator

# from .slot import CreateSlot
from sqlalchemy.orm import Session  # type: ignore

from .. import app_exceptions, crud, db, models
from . import slots, users, workers
from .slots import CreateSlot, TimeSlot, TimeSlotType


class Day(BM):
    """Both in and Out"""

    date: datetime.date
    timeslots: list[TimeSlot]


DAYS = {0: "mo", 1: "tu", 2: "we", 3: "th", 4: "fr", 5: "st", 6: "su"}
N_DAYS = 99
DAY_START_TIME = datetime.time(hour=0, minute=0)


class Availability(BM):
    # by day to easily map to calendar
    days: list[Day]

    @classmethod
    def CreateFromSchedule(
        cls, schedule: dict[str, Any], n_days: int = N_DAYS
    ) -> "Availability":  # optional schedule
        """creates TimeSlots from Schedule"""
        days = []
        today = datetime.date.today()

        for day_delta in range(n_days):
            target_day = today + datetime.timedelta(days=day_delta)
            weekday = DAYS[target_day.weekday()]
            list_from_to = schedule[weekday] if schedule else []
            if not list_from_to:
                continue

            timeslots = []
            for l in list_from_to:
                time_from = datetime.datetime.strptime(l[0], "%H:%M")
                time_to = datetime.datetime.strptime(l[1], "%H:%M")
                dt_from = datetime.datetime.combine(target_day, time_from.time())
                dt_to = datetime.datetime.combine(target_day, time_to.time())
                timeslots.append(
                    TimeSlot(
                        dt_from=dt_from,
                        dt_to=dt_to,
                        slot_type=TimeSlotType.AVAILABLE,
                    )
                )
            day = Day(date=target_day, timeslots=timeslots)
            days.append(day)
        return cls(days=days)

    @classmethod
    def CreateFromSlots(cls, slots: list[models.Slot]) -> "Availability":
        days: dict[datetime.date, Day] = {}
        for slot in slots:
            assert slot.slot_type == TimeSlotType.AVAILABLE
            assert (
                slot.to_datetime - slot.from_datetime
            ).total_seconds() <= 60 * 60 * 24, "slot length should be below 24h"

            slot_from_date = slot.from_datetime.date()
            if slot_from_date in days:
                day = days[slot_from_date]
            else:
                day = Day(date=slot_from_date, timeslots=[])

            day.timeslots.append(
                TimeSlot(
                    dt_from=slot.from_datetime,
                    dt_to=slot.to_datetime,
                    slot_type=TimeSlotType(slot.slot_type),
                )
            )
            days[slot_from_date] = day

            slot_to_date = slot.to_datetime.date()
            if slot_to_date != slot_from_date:
                if slot_to_date in days:
                    day = days[slot_to_date]
                else:
                    day = Day(date=slot_to_date, timeslots=[])

                # day should start from 00:00
                day_start = datetime.datetime.combine(slot_to_date, DAY_START_TIME)
                day.timeslots.append(
                    TimeSlot(
                        dt_from=day_start,
                        dt_to=slot.to_datetime,
                        slot_type=TimeSlotType(slot.slot_type),
                    )
                )
                days[slot_to_date] = day

        days_l = list(days.values())
        return cls(days=days_l)

    # def IncreaseAvailabilityBySlots(
    #     self, slots: list[models.Slot]):

    def ReduceAvailabilityBySlots(self, slots: list[models.Slot]) -> None:
        """Reduces timeslots by busy/visit slots"""
        # need assure sort
        # @speed - sorted version
        days = self.days
        for slot in slots:
            assert slot.slot_type in [TimeSlotType.BUSY, TimeSlotType.VISIT]

            for iday, day in enumerate(days):
                new_ts = []
                date = day.date
                # if the slot is not an overnight one - skip it
                if not (slot.from_datetime.date() == date or slot.to_datetime.date() == date):
                    continue

                for its, ts in enumerate(day.timeslots):
                    f = ts.dt_from
                    t = ts.dt_to

                    F = slot.from_datetime
                    T = slot.to_datetime

                    # need to add quick filter

                    # f, t - ts
                    # F, T   - slot
                    # _ - availability

                    # slot is bigger than schedule slot
                    #  f t
                    # F    T
                    if F <= f and T >= t:
                        # we remove availability
                        continue

                    if F > t:
                        new_ts.append(
                            TimeSlot(dt_from=ts.dt_from, dt_to=ts.dt_to, slot_type=ts.slot_type)
                        )
                        continue

                    if T < f:
                        new_ts.append(
                            TimeSlot(dt_from=ts.dt_from, dt_to=ts.dt_to, slot_type=ts.slot_type)
                        )
                        continue

                    # left is less, right in
                    #  f   __t
                    # F   T
                    if F <= f and T < t:
                        new_ts.append(
                            TimeSlot(dt_from=T, dt_to=t, slot_type=TimeSlotType.AVAILABLE)
                        )

                    # right is bigger, left is in
                    # f__   t
                    #    F   T
                    if F > f and T >= t:
                        new_ts.append(
                            TimeSlot(dt_from=f, dt_to=F, slot_type=TimeSlotType.AVAILABLE)
                        )

                    # slot is in
                    # f_  _t
                    #   FT
                    if F > f and T < t:
                        # we create 2 slots for that
                        new_ts.append(
                            TimeSlot(dt_from=f, dt_to=F, slot_type=TimeSlotType.AVAILABLE)
                        )
                        new_ts.append(
                            TimeSlot(dt_from=T, dt_to=t, slot_type=TimeSlotType.AVAILABLE)
                        )
                        # above copies left-right checks, can make it simplier

                day.timeslots = new_ts
                days[iday] = day

        self.days = days

    def SplitByLengthAndTrim(self, length_minutes: int) -> None:
        for iday, day in enumerate(self.days):
            day.date
            timeslots = day.timeslots

            new_timeslots: list[TimeSlot] = []
            for timeslot in timeslots:
                delta = (timeslot.dt_to - timeslot.dt_from).total_seconds() / 60
                n_by_len = delta / length_minutes
                n_by_len = math.floor(n_by_len)
                for n in range(n_by_len):
                    new_dt_from = timeslot.dt_from + (
                        datetime.timedelta(minutes=length_minutes * n)
                    )
                    new_dt_to = timeslot.dt_from + (
                        datetime.timedelta(minutes=length_minutes * (n + 1))
                    )
                    new_slot = TimeSlot(
                        dt_from=new_dt_from,
                        dt_to=new_dt_to,
                        slot_type=TimeSlotType.AVAILABLE,
                    )
                    new_timeslots.append(new_slot)

            day.timeslots = new_timeslots
            self.days[iday] = day
        return

    def CheckSlot(self, slot: "CreateSlot") -> bool:
        assert slot.slot_type == "visit"
        for day in self.days:
            prev_t: Optional[TimeSlot] = None
            for t in day.timeslots:
                if prev_t and prev_t.dt_to == t.dt_from:
                    # extending t, building an availability
                    t.dt_from = prev_t.dt_from

                if t.dt_from <= slot.from_datetime and slot.to_datetime <= t.dt_to:
                    return True

                prev_t = t

        return False

    @classmethod
    def WorkersToClient(cls, avs: list["Availability"]) -> "Availability":
        raise NotImplemented
        # """Returns availabiltiy of client, which may consist of colliding worker timeslots"""
        # days = collections.defaultdict(list)
        # for av in avs:
        #     for day in av.days:
        #         date = day.date
        #         days[date].extend(day.timeslots)
        # days_l = []
        # for date, timeslots in days.items():
        #     reduced = set(timeslots)
        #     reduced_timeslots = list(reduced)
        #     reduced_timeslots.sort()
        #     d = Day(date=date, timeslots=reduced_timeslots)
        #     days_l.append(d)

        # return cls(days=days_l)

    @classmethod
    def GetWorkerAV(
        cls,
        s: Session,
        worker_id: int,  # assumed that id is real already
        *,
        visit_length: Optional[int] = None,
        _from: datetime.date | None = None
    ) -> "WorkerAvailability":
        _from = _from or datetime.date.today()

        slots = crud.get_worker_slots(
            s, worker_id=worker_id, slot_types=[TimeSlotType.AVAILABLE], _from=_from
        )
        av = cls.CreateFromSlots(slots)

        busy_slots = crud.get_worker_slots(
            s, worker_id, slot_types=[TimeSlotType.BUSY, TimeSlotType.VISIT]
        )
        av.ReduceAvailabilityBySlots(busy_slots)
        if visit_length:
            av.SplitByLengthAndTrim(length_minutes=visit_length)
        return WorkerAvailability(days=av.days, worker_id=worker_id)

    def EnsureEmptyDays(
        self,
        _from: datetime.date,
        _to: datetime.date,
    ) -> None:
        self.days.sort(key=(lambda day: day.date))
        while _from <= _to:
            date = _from
            _from += datetime.timedelta(days=1)

            empty = Day(date=date, timeslots=[])

            for i_day, day in enumerate(self.days):
                if date == day.date:
                    break
                if day.date > date:
                    self.days.insert(i_day, empty)
                    break
            else:
                self.days.append(empty)

    def TrimTo(
        self,
        _to: datetime.date,
    ) -> None:
        new_days = []
        for day in self.days:
            if day.date > _to:
                continue
            new_days.append(day)
        self.days = new_days


class WorkerAvailability(Availability):
    worker_id: int


class AvailabilityPerWorker(BM):
    availability: list[WorkerAvailability]


def _get_client_availability(
    client_id: int,
    service_length: Optional[int],
    service_ids: list[int],
    s: Session,
) -> list[WorkerAvailability]:
    if service_ids:
        workers = crud.get_skilled_workers(s, client_id, service_ids)
    else:
        workers = crud.get_workers(s, client_id)

    worker_avs = []
    for worker in workers:
        av = Availability.GetWorkerAV(s, worker.worker_id, visit_length=service_length)
        worker_avs.append(av)
    return worker_avs


def visit_pick_worker_or_throw(
    s: Session, slot: CreateSlot, client_id: int, *, exc: HTTPException, force: bool = False
) -> CreateSlot:
    # force flag
    # - if worker is picked - override slot check
    # - if worker is not picked - raise, use is forced to pick worker
    # (?) this might not work well if there is only single worker

    _worker_id = slot.worker_id

    workers = crud.get_workers(s, client_id)
    if len(workers) == 1:
        _worker_id = workers[0].worker_id

    if _worker_id:
        worker_id = _worker_id
        av = Availability.GetWorkerAV(s, worker_id)
        if not av.CheckSlot(slot):
            if not force:
                raise exc
    else:
        all_av = _get_client_availability(client_id, None, [s.service_id for s in slot.services], s)
        available_av = [av for av in all_av if av.CheckSlot(slot)]
        if len(available_av) == 0:
            raise exc
        worker_av = random.choice(available_av)
        slot.worker_id = worker_av.worker_id

    if not slot.worker_id:
        raise ValueError("worker id was not set")

    return slot


def get_worker_availability(
    client_id: str = Path(regex=r"\d+"),
    worker_id: str = Path(regex=r"\d+"),
    from_date: datetime.date | None = Query(None),
    services: str | None = Query(None),
    s: Session = Depends(db.get_session),
) -> Availability:
    return _get_worker_availability(client_id, worker_id, from_date, services, s)


def get_worker_availability_by_user(
    worker_id: str = Path(regex=r"\d+"),
    from_date: datetime.date | None = Query(None),
    services: str | None = Query(None),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Availability:
    return _get_worker_availability(str(current_user.client_id), worker_id, from_date, services, s)


def _get_worker_availability(
    client_id: str,
    worker_id: str,
    from_date: datetime.date | None,
    services: str | None,
    s: Session,
) -> Availability:
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        db_worker_services = crud.get_services(
            s, client_id=int(client_id), worker_id=int(worker_id)
        )
        for service in db_services:
            if service not in db_worker_services:
                raise app_exceptions.WorkerNotSkilled
        total_service_length = sum([s.minutes for s in db_services])
        av = Availability.GetWorkerAV(
            s, int(worker_id), visit_length=total_service_length, _from=from_date
        )
    else:
        # when requesting for availability we populate empty days for calendar
        _from = from_date or datetime.date.today()
        _from_monday = _prev_monday(_from)
        _end_of_month_monday = _next_monday(
            _from + relativedelta(months=1) - datetime.timedelta(days=1)
        )
        av = Availability.GetWorkerAV(s, int(worker_id), visit_length=None, _from=_from_monday)
        av.TrimTo(_end_of_month_monday)
        av.EnsureEmptyDays(_from_monday, _end_of_month_monday)
    return av


def _prev_monday(d: datetime.date) -> datetime.date:
    while d.isoweekday() != 1:
        d -= datetime.timedelta(days=1)
    return d


def _next_monday(d: datetime.date) -> datetime.date:
    while d.isoweekday() != 1:
        d += datetime.timedelta(days=1)
    return d


def get_client_availability(
    client_id: int,
    services: Optional[str] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> AvailabilityPerWorker:
    total_service_length = None
    service_ids = []
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        total_service_length = sum([s.minutes for s in db_services])

    d = _get_client_availability(client_id, total_service_length, service_ids, s)
    return AvailabilityPerWorker(availability=d)


def create_worker_availability(
    worker_id: str,
    r: Availability,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> None:
    # safety
    workers.assure_worker_and_owner(s, current_user, worker_id)

    # we delete existing av's
    dates = [d.date for d in r.days]
    slots.delete_available_slots(dates, int(worker_id), s, current_user)
    # then create new ones
    new_slots_schemas = []
    for d in r.days:
        for t in d.timeslots:
            new_slots_schemas.append(
                slots.CreateSlot.Available(
                    worker_id=int(worker_id),
                    from_datetime=t.dt_from,
                    to_datetime=t.dt_to,
                )
            )
    slots.create_slots(current_user.client_id, new_slots_schemas, s)
