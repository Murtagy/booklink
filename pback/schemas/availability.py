import datetime
import math
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel as BM

# from .slot import CreateSlot
from sqlalchemy.orm import Session

import crud
import models


class TimeSlotType(str, Enum):
    BUSY = "busy"
    AVAILABLE = "available"
    VISIT = "visit"


class TimeSlot(BM):
    dt_from: datetime.datetime
    dt_to: datetime.datetime
    slot_type: TimeSlotType

    def __str__(self):
        return str(self.dt_from) + ":::" + str(self.dt_to) + " " + str(self.slot_type)

    def __hash__(self):
        return hash(str(self))

    def __gt__(self, other):
        return self.dt_from > other.dt_from


class Day(BM):
    date: datetime.date
    timeslots: list[TimeSlot]


DAYS = {0: "mo", 1: "tu", 2: "we", 3: "th", 4: "fr", 5: "st", 6: "su"}
N_DAYS = 99


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
            # print(list_from_to)
            if not list_from_to:
                continue
            timeslots = []
            for l in list_from_to:
                # print(l)
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
    def CreateFromSlots(cls, slots: list[models.Slot]):
        days: dict[datetime.date, Day] = {}
        for slot in slots:
            # print(slot.slot_type)
            assert slot.slot_type == TimeSlotType.AVAILABLE
            slot_from_date = slot.from_datetime.date()
            if slot_from_date in days:
                day = days[slot_from_date]
            else:
                day = Day(date=slot_from_date, timeslots=[])

            day.timeslots.append(
                TimeSlot(
                    dt_from=slot.from_datetime,
                    dt_to=slot.to_datetime,
                    slot_type=slot.slot_type,
                )
            )
            days[slot_from_date] = day

        days_l = list(days.values())
        return cls(days=days_l)

    # def IncreaseAvailabilityBySlots(
    #     self, slots: list[models.Slot]):

    def ReduceAvailabilityBySlots(self, slots: list[models.Slot]) -> None:
        """Reduces timeslots by busy/visit slots"""
        # need assure sort
        # @speed - sorted version
        # print("Reducing")
        days = self.days
        # print(slots)
        for slot in slots:
            # print("Slot", slot.from_datetime, slot.to_datetime)
            assert slot.slot_type in [TimeSlotType.BUSY, TimeSlotType.VISIT]
            for iday, day in enumerate(days):
                # print(day.date)
                new_ts = []
                date = day.date
                if not slot.from_datetime.date() <= date <= slot.to_datetime.date():
                    continue

                # print("Not skipped")
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
                    if F < f and T > t:
                        continue

                    # left is less, right in
                    #  f   __t
                    # F   T
                    if F < f and T < t:
                        new_ts.append(
                            TimeSlot(
                                dt_from=T, dt_to=t, slot_type=TimeSlotType.AVAILABLE
                            )
                        )

                    # right is bigger, left is in
                    # f__   t
                    #    F   T
                    if F > f and T > t:
                        new_ts.append(
                            TimeSlot(
                                dt_from=f, dt_to=F, slot_type=TimeSlotType.AVAILABLE
                            )
                        )

                    # slot is in
                    # f_  _t
                    #   FT
                    if F > f and T < t:
                        # print("SLOT IN")
                        # we create 2 slots for that
                        new_ts.append(
                            TimeSlot(
                                dt_from=f, dt_to=F, slot_type=TimeSlotType.AVAILABLE
                            )
                        )
                        new_ts.append(
                            TimeSlot(
                                dt_from=T, dt_to=t, slot_type=TimeSlotType.AVAILABLE
                            )
                        )
                        # above copies left-right checks, can make it simplier

                day.timeslots = new_ts
                days[iday] = day

        self.days = days

    def SplitByLength(self, length_seconds: int):
        for iday, day in enumerate(self.days):
            date = day.date
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

    def CheckSlot(self, slot) -> bool:
        assert slot.slot_type == "visit"
        for day in self.days:
            prev_t = None
            for t in day.timeslots:
                if prev_t and prev_t.dt_to == t.dt_from:
                    # extending t, building an availability 
                    t.dt_from = prev_t.dt_from

                if t.dt_from <= slot.from_datetime and slot.to_datetime <= t.dt_to:
                    return True

                prev_t = t

        return False

    @classmethod
    def WorkersToClient(cls, avs: list["Availability"]):
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
    async def GetWorkerAV(
        cls,
        s: Session,
        worker_u: Union[int, models.Worker],
        *,
        service_length: Optional[int] = None,
    ) -> "Availability":
        Availability = cls
        if isinstance(worker_u, int):
            worker = crud.get_worker(s, worker_u)
            assert worker is not None
        else:
            worker = worker_u

        if worker.use_company_schedule:
            wl = crud.get_client_weeklyslot(s, worker.client_id)
            assert wl
            assert isinstance(wl.schedule_by_day, dict)
            av = Availability.CreateFromSchedule(wl.schedule_by_day)
        else:
            wl = crud.get_worker_weeklyslot(s, worker.worker_id)
            if wl is not None:
                assert isinstance(wl.schedule_by_day, dict)
                av = Availability.CreateFromSchedule(wl.schedule_by_day)
            else:
                slots = crud.get_worker_slots(
                    s, worker_id=worker.worker_id, slot_types=[TimeSlotType.AVAILABLE]
                )
                av = Availability.CreateFromSlots(slots)

        busy_slots = crud.get_worker_slots(
            s, worker.worker_id, slot_types=[TimeSlotType.BUSY, TimeSlotType.VISIT]
        )
        av.ReduceAvailabilityBySlots(busy_slots)
        if service_length:
            av.SplitByLength(length_seconds=service_length)
        return av


async def _get_client_availability(
    client_id: int,
    service_length: Optional[int],
    s: Session,
) -> dict[int, Availability]:
    workers = crud.get_workers(s, client_id)
    worker_avs: dict[int, Availability] = {}
    for worker in workers:
        av = await Availability.GetWorkerAV(s, worker, service_length=service_length)
        worker_avs[worker.worker_id] = av
    return worker_avs


class AvailabilityPerWorker(BM):
    availability: dict[int, Availability]

    @classmethod
    def FromDict(cls, availability: dict[int, Availability]):
        return cls(availability=availability)
