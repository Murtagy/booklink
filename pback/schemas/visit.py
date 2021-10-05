from pydantic import BaseModel as BM

from typing import Literal, List



class InServiceToVisit(BM):
    name: str
    price: float
    q: int
    worker: str
    timeslot: str

class OutVisit(BM):
    status: str
    # cp
    version: Literal[1]
    phone: str
    client_id: str
    services: List[InServiceToVisit]

    @classmethod
    def Example(cls):
        return cls(
            status='status',
            version=1,
            phone='375291231123',
            client_id='client_id',
            services=[],
        )



class InVisit(BM):
    version: Literal[1]
    phone: str
    email: str
    client_id: str
    services: List[InServiceToVisit]
    remind_me: bool


# class VisitStatus(SEnum):
#     SUMBITTED = 'SUBMITTED'  # -> R/A
#     REJECTED = 'REJECTED'
#     APPROVED = 'APPROVED'  # -> C
#     CANCELLED = 'CANCELLED'
#     # MISSED = 'MISSED'
#     # FINISHED = 'FINISHED'
