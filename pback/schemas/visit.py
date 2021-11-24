import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel as BM


class InServiceToVisit(BM):
    name: str
    price: float
    q: int
    worker: str
    timeslot: str


class OutVisit(BM):
    version: Literal[1] = 1
    phone: str
    # from_dt: datetime.datetime
    # to_dt: datetime.datetime

    class Config:
        orm_mode = True
        # make this inherited?

    @classmethod
    def Example(cls):
        return cls(
            status="status",
            phone="375291231123",
            client_id=123,
            # services=[],
        )


class InVisit(BM):
    version: Literal[1]
    from_dt: datetime.datetime
    to_dt: datetime.datetime
    phone: str
    email: str
    client_id: int
    worker_id: Optional[int]
    services: List[InServiceToVisit]
    remind_me: bool


# class VisitStatus(SEnum):
#     SUMBITTED = 'SUBMITTED'  # -> R/A
#     REJECTED = 'REJECTED'
#     APPROVED = 'APPROVED'  # -> C
#     CANCELLED = 'CANCELLED'
#     # MISSED = 'MISSED'
#     # FINISHED = 'FINISHED'
