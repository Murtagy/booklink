from models import Slot
from .availability import Availability
import datetime


def test_av():
    # setting now to 9 pm (av slots created are overnight)
    time = datetime.datetime(year=2023, month=1, day=1, hour=21)

    availability_5h = Slot(
        slot_id=1,
        name='Day',
        slot_type='available',
        from_datetime=time,
        to_datetime=time + datetime.timedelta(hours=5),
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
        name='Visit',
        slot_type='visit',
        from_datetime=time,
        to_datetime=time + datetime.timedelta(hours=1),
        worker_id=1,
        client_id=1,
    )
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1
    assert av.days[0].timeslots[0].dt_from == time + datetime.timedelta(hours=1)
    assert av.days[0].timeslots[0].dt_to == time + datetime.timedelta(hours=5)
    assert av.days[0].timeslots[0].slot_type == 'available'

    # 1h visit in the middle of availability, av splits in 2
    av = Availability.CreateFromSlots(slots)
    visit_1h.from_datetime = time + datetime.timedelta(hours=1)
    visit_1h.to_datetime = time + datetime.timedelta(hours=2)
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 2
    assert av.days[0].timeslots[0].dt_from == time
    assert av.days[0].timeslots[0].dt_to == time + datetime.timedelta(hours=1)
    assert av.days[0].timeslots[1].dt_from == time + datetime.timedelta(hours=2)
    assert av.days[0].timeslots[1].dt_to == time + datetime.timedelta(hours=5)

    # 1h visit in the end of availability, av shifts left
    av = Availability.CreateFromSlots(slots)
    visit_1h.from_datetime = time + datetime.timedelta(hours=4)
    visit_1h.to_datetime = time + datetime.timedelta(hours=5)
    av.ReduceAvailabilityBySlots(slots=[visit_1h])
    assert len(av.days) == 2
    assert len(av.days[0].timeslots) == 1

    # TMP, not sure how to handle overnight availability / visits

    # today - not changed
    assert av.days[0].timeslots[0].dt_from == time 
    assert av.days[0].timeslots[0].dt_to == time + datetime.timedelta(hours=5)
    assert av.days[0].timeslots[0].slot_type == 'available'
    # tomorrow - to dt reduced
    assert av.days[1].timeslots[0].dt_to == time + datetime.timedelta(hours=4)
    assert av.days[1].timeslots[0].slot_type == 'available'
