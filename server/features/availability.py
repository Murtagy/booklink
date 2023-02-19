import datetime
import math
import random
from typing import Any, Optional, Union

from fastapi import Depends, Path, Query
from fastapi.exceptions import HTTPException
from pydantic import BaseModel as BM

# from .slot import CreateSlot
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions
import crud
import db
import models
from features.slots import CreateSlot, TimeSlot, TimeSlotType


class Day(BM):
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

    def SplitByLengthAndTrim(self, length_seconds: int) -> None:
        for iday, day in enumerate(self.days):
            day.date
            timeslots = day.timeslots

            new_timeslots: list[TimeSlot] = []
            for timeslot in timeslots:
                delta = (timeslot.dt_to - timeslot.dt_from).total_seconds() / 60
                length_minutes = length_seconds / 60
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
        worker_u: Union[int, models.Worker],
        *,
        service_length: Optional[int] = None,
    ) -> "WorkerAvailability":
        if isinstance(worker_u, int):
            worker = crud.get_worker(s, worker_u)
            assert worker is not None
        else:
            worker = worker_u

        slots = crud.get_worker_slots(
            s, worker_id=worker.worker_id, slot_types=[TimeSlotType.AVAILABLE]
        )
        av = cls.CreateFromSlots(slots)

        busy_slots = crud.get_worker_slots(
            s, worker.worker_id, slot_types=[TimeSlotType.BUSY, TimeSlotType.VISIT]
        )
        av.ReduceAvailabilityBySlots(busy_slots)
        if service_length:
            av.SplitByLengthAndTrim(length_seconds=service_length)
        return WorkerAvailability(days=av.days, worker_id=worker.worker_id)


class WorkerAvailability(Availability):
    worker_id: int


class AvailabilityPerWorker(BM):
    availability: list[WorkerAvailability]


def _get_client_availability(
    client_id: int,
    service_length: Optional[int],
    s: Session,
) -> list[WorkerAvailability]:
    workers = crud.get_workers(s, client_id)
    worker_avs = []
    for worker in workers:
        av = Availability.GetWorkerAV(s, worker, service_length=service_length)
        worker_avs.append(av)
    return worker_avs


def visit_pick_worker_or_throw(s: Session, slot: CreateSlot, *, exc: HTTPException) -> CreateSlot:
    _worker_id = slot.worker_id
    if _worker_id:
        worker_id = _worker_id
        av = Availability.GetWorkerAV(s, worker_id)
        if not av.CheckSlot(slot):
            raise exc

    else:
        client_av = _get_client_availability(slot.client_id, None, s)
        available_workers_av = [av for av in client_av if av.CheckSlot(slot)]
        if len(available_workers_av) == 0:
            raise exc

        worker_av = random.choice(available_workers_av)
        slot.worker_id = worker_av.worker_id
    return slot


def get_worker_availability(
    client_id: str,
    worker_id: str = Path(regex=r"\d+"),
    services: str | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> Availability:
    worker = crud.get_worker(s, int(worker_id))
    assert worker is not None

    total_service_length: Optional[int] = None
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        db_worker_services = crud.get_services(
            s, client_id=worker.client_id, worker_id=int(worker_id)
        )
        for service in db_services:
            if service not in db_worker_services:
                raise app_exceptions.WorkerNotSkilled
        total_service_length = sum([s.seconds for s in db_services])
    av = Availability.GetWorkerAV(s, worker, service_length=total_service_length)
    return av


def get_client_availability(
    client_id: int,
    services: Optional[str] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> AvailabilityPerWorker:
    total_service_length = None
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        total_service_length = sum([s.seconds for s in db_services])

    d = _get_client_availability(client_id, total_service_length, s)
    return AvailabilityPerWorker(availability=d)
