import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel as BM


class InServiceToVisit(BM):
    service_id: int


class OutVisit(BM):
    version: Literal[1] = 1
    phone: str
    # from_dt: datetime.datetime
    # to_dt: datetime.datetime

    class Config:
        orm_mode = True
        # make this inherited?

    @classmethod
    def Example(cls) -> 'OutVisit':
        return cls(
            phone="375291231123",
        )


class InVisit(BM):
    client_id: int
    from_dt: datetime.datetime
    # to_dt: datetime.datetime
    email: str
    services: List[InServiceToVisit]
    phone: str
    remind_me: bool
    version: Literal[1] = 1
    worker_id: Optional[int]


# class VisitStatus(SEnum):
#     SUMBITTED = 'submitted'  # -> R/A
#     REJECTED = 'rejected'
#     APPROVED = 'approved'  # -> C
#     CANCELLED = 'cancelled'
#     # MISSED = 'missed'
#     # FINISHED = 'finished'
