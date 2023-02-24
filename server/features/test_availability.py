import datetime

from ..models import Slot
from .availability import Availability

hour = datetime.timedelta(hours=1)
minute = datetime.timedelta(minutes=1)


def test_av_create_from_slots():
    time = datetime.datetime(year=2023, month=1, day=1, hour=12)
    availability_8h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (8 * hour),
        worker_id=1,
        client_id=1,
    )
    av = Availability.CreateFromSlots([availability_8h])
    assert len(av.days) == 1
    assert av.days[0].date == time.date()
    assert len(av.days[0].timeslots) == 1
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (8 * hour)


def test_av_single_visit():
    # setting now to 9 pm (av slots created are overnight)
    time = datetime.datetime(year=2023, month=1, day=1, hour=21)

    availability_5h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (5 * hour),
        worker_id=1,
        client_id=1,
    )
    slots = [availability_5h]
    av = Availability.CreateFromSlots(slots)
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1

    # 1h visit in the start of availability, av shifts right
    visit_1h = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time,
        to_datetime=time + (1 * hour),
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1
    assert av.days[0].timeslots[0].dt_from == time + hour
    assert av.days[0].timeslots[0].dt_to == time + (5 * hour)
    assert av.days[0].timeslots[0].slot_type == "available"

    # 1h visit in the middle of availability, av splits in 2
    av = Availability.CreateFromSlots(slots)
    visit_1h.from_datetime = time + hour
    visit_1h.to_datetime = time + (2 * hour)
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 2
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (1 * hour)
    assert av.days[0].timeslots[1].dt_from == time + (2 * hour)
    assert av.days[0].timeslots[1].dt_to == time + (5 * hour)

    # 1h visit in the end of availability, av shifts left
    av = Availability.CreateFromSlots(slots)
    visit_1h.from_datetime = time + (4 * hour)
    visit_1h.to_datetime = time + (5 * hour)
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1

    # TMP, not sure how to handle overnight availability / visits

    # today - not changed
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (5 * hour)
    assert av.days[0].timeslots[0].slot_type == "available"
    # tomorrow - to dt reduced
    assert av.days[1].timeslots[0].dt_from == time + (3 * hour)  # day should start from 00:00
    assert av.days[1].timeslots[0].dt_to == time + (4 * hour)
    assert av.days[1].timeslots[0].slot_type == "available"


def test_av_2_visits():
    time = datetime.datetime(year=2023, month=1, day=1, hour=8)
    availability_5h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (8 * hour),
        worker_id=1,
        client_id=1,
    )
    slots = [availability_5h]

    # 45 min slot x2 next to each other
    av = Availability.CreateFromSlots(slots)
    visit_45min = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time,
        to_datetime=time + (45 * minute),
        worker_id=1,
        client_id=1,
    )
    visit_45min_2 = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time + (45 * minute),
        to_datetime=time + (45 * minute) + (45 * minute),
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_45min, visit_45min_2])
    assert av.days[0].timeslots[0].dt_from == time + (45 * minute) + (45 * minute)
    assert av.days[0].timeslots[0].dt_to == time + (8 * hour)

    av = Availability.CreateFromSlots(slots)
    # 45 min slot x2 with 45 min gap
    visit_45min_2.from_datetime = time + ((45 * minute) * 2)
    visit_45min_2.to_datetime = time + ((45 * minute) * 3)
    av.ReduceAvailabilityBySlots(slots=[visit_45min, visit_45min_2])
    assert av.days[0].timeslots[0].dt_from == time + (45 * minute)
    assert av.days[0].timeslots[0].dt_to == time + ((45 * minute) * 2)


def test_av_split():
    # setting now to 9 pm (av slots created are overnight)
    time = datetime.datetime(year=2023, month=1, day=1, hour=21)

    availability_5h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (5 * hour),
        worker_id=1,
        client_id=1,
    )
    slots = [availability_5h]
    av = Availability.CreateFromSlots(slots)
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1

    # full fill test - 5h services
    av.SplitByLengthAndTrim(5 * 60)
    assert len(av.days[0].timeslots) == 1
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (5 * hour)

    # basic test - 45 min slots
    # 1h visit in the start of availability, av shifts right
    av = Availability.CreateFromSlots(slots)
    visit_1h = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time,
        to_datetime=time + (1 * hour),
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    av.SplitByLengthAndTrim(45)
    assert av.days[0].timeslots[0].dt_from == time + (1 * hour)
    assert av.days[0].timeslots[0].dt_to == time + (1 * hour) + (45 * minute)

    # 44 min slot placed one close to another
    av = Availability.CreateFromSlots(slots)
    visit_44min = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time + (1 * hour),
        to_datetime=time + (1 * hour) + (44 * minute),
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_1h, visit_44min])
    av.SplitByLengthAndTrim(45)
    assert av.days[0].timeslots[0].dt_from == time + (1 * hour) + (44 * minute)
    assert av.days[0].timeslots[0].dt_to == time + (1 * hour) + (44 * minute) + (45 * minute)

    # 45 min slot placed after 44 min
    av = Availability.CreateFromSlots(slots)
    visit_44min.from_datetime = time + (1 * hour) + (44 * minute)
    visit_44min.to_datetime = time + (1 * hour) + (44 * minute) + (45 * minute)
    av.ReduceAvailabilityBySlots(slots=[visit_1h, visit_44min])
    av.SplitByLengthAndTrim(45)
    assert av.days[0].timeslots[0].dt_from == time + (1 * hour) + (44 * minute) + (45 * minute)
    assert av.days[0].timeslots[0].dt_to == time + (1 * hour) + (44 * minute) + (45 * minute) + (
        45 * minute
    )


def test_av_split_():
    time = datetime.datetime(year=2023, month=1, day=1, hour=12)

    availability_5h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (5 * hour),
        worker_id=1,
        client_id=1,
    )
    slots = [availability_5h]
    av = Availability.CreateFromSlots(slots)
    # 2 slots before start of av (for example manually added)
    visit_45min = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time - (2 * hour),
        to_datetime=time - (1 * hour),
        worker_id=1,
        client_id=1,
    )
    visit_45min_2 = Slot(
        slot_id=1,
        name="Visit",
        slot_type="visit",
        from_datetime=time - (1 * hour),
        to_datetime=time,
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_45min, visit_45min_2])
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (5 * hour)
    assert len(av.days[0].timeslots) == 1
    av.SplitByLengthAndTrim(45)
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + (45 * minute)
    assert len(av.days[0].timeslots) == 6
