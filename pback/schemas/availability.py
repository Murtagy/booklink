import collections
import datetime
import math
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel as BM

import models


class TimeSlotType(str, Enum):
    BUSY = "busy"
    AVAILABLE = "available"
    VISIT = "visit"


class TimeSlot(BM):
    dt_from: datetime.datetime
    dt_to: datetime.datetime
    slot_type: TimeSlotType


class Day(BM):
    date: datetime.date
    timeslots: List[TimeSlot]


DAYS = {0: "mo", 1: "tu", 2: "we", 3: "th", 4: "fr", 5: "st", 6: "su"}
N_DAYS = 99


class Availability(BM):
    # by day to easily map to calendar
    days: List[Day]

    @classmethod
    def CreateFromSchedule(
        cls, schedule: Dict[str, Any], n_days: int = N_DAYS
    ) -> "Availability":  # optional schedule
        """creates TimeSlots from Schedule"""
        days = []
        today = datetime.date.today()
        for day_delta in range(n_days):
            target_day = today + datetime.timedelta(days=day_delta)
            weekday = DAYS[target_day.weekday()]
            list_from_to = schedule[weekday] if schedule else []
            print(list_from_to)
            if not list_from_to:
                continue
            timeslots = []
            for l in list_from_to:
                print(l)
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
    def CreateFromSlots(cls, slots: List[models.Slot]):
        days: Dict[datetime.date, Day] = {}
        for slot in slots:
            assert slot.slot_type == TimeSlotType.AVAILABLE
            slot_from_date = slot.from_datetime.date()
            if slot_from_date in days:
                day = days[slot_from_date]
            else:
                day = Day(date=slot_from_date, timeslots=[])

            day.timeslots.append(
                TimeSlot(
                    from_dt=slot.from_datetime,
                    to_dt=slot.to_datetime,
                    slot_type=slot.slot_type,
                )
            )
            days[slot_from_date] = day

        days_l = list(days.values())
        return cls(days=days_l)

    # def IncreaseAvailabilityBySlots(
    #     self, slots: List[models.Slot]):

    def ReduceAvailabilityBySlots(self, slots: List[models.Slot]) -> None:
        """Reduces timeslots by busy/visit slots"""
        # need assure sort
        # @speed - sorted version
        print("Reducing")
        days = self.days
        print(slots)
        for slot in slots:
            print("Slot", slot.from_datetime, slot.to_datetime)
            assert slot.slot_type in [TimeSlotType.BUSY, TimeSlotType.VISIT]
            for iday, day in enumerate(days):
                print(day.date)
                new_ts = []
                date = day.date
                if not slot.from_datetime.date() <= date <= slot.to_datetime.date():
                    continue

                print("Not skipped")
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
                        print("SLOT IN")
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

            new_timeslots: List[TimeSlot] = []
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

    @classmethod
    def WorkersToClient(cls, avs: List["Availability"]):
        """Returns availabiltiy of client, which may consist of colliding worker timeslots"""
        days = collections.defaultdict(list)
        for av in avs:
            for day in av.days:
                date = day.date
                days[date].extend(day.timeslots)
        days_l = []
        for date, timeslots in days.items():
            d = Day(date=date, timeslots=timeslots)
            days_l.append(d)

        return cls(days=days_l)
