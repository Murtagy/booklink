import datetime

from ..models import Slot, Worker
from .slots import AllSlots

hour = datetime.timedelta(hours=1)
minute = datetime.timedelta(minutes=1)


def test_all_slots():
    time = datetime.datetime(year=2023, month=1, day=1, hour=12)
    worker1 = Worker(worker_id=1, client_id=1, name="Maks", job_title="Job")
    # 1 worker 1 day
    availability_8h = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time,
        to_datetime=time + (8 * hour),
        worker_id=1,
        client_id=1,
    )
    visit_45min = Slot(
        slot_id=2,
        name="Visit",
        slot_type="visit",
        from_datetime=time,
        to_datetime=time + (45 * minute),
        worker_id=1,
        client_id=1,
    )
    all_slots = AllSlots.FromSlots([availability_8h], [worker1])
    assert len(all_slots.days) == 1

    # 1 worker, 2 days
    availability_8h_tmr = Slot(
        slot_id=1,
        name="Day",
        slot_type="available",
        from_datetime=time + (24 * hour),
        to_datetime=time + (8 * hour) + (24 * hour),
        client_id=1,
        worker_id=1,
    )

    all_slots = AllSlots.FromSlots([availability_8h, availability_8h_tmr], [worker1])
    assert len(all_slots.days) == 2
