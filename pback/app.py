from typing import List, Literal
from fastapi import FastAPI

from pydantic import BaseModel as BM

import datetime
from enum import Enum

app = FastAPI()

class SEnum(str, Enum):
    ...


# FXxx - from client

class FServiceToVisit(BM):
    name: str
    price: float
    q: int
    worker: str
    timeslot: str

class FVisit(BM):
    version: Literal[1]
    phone: str
    email: str
    client_id: str
    services: List[FServiceToVisit]
    remind_me: bool


class VisitStatus(SEnum):
    SUMBITTED = 'SUBMITTED'  # -> R/A
    REJECTED = 'REJECTED'
    APPROVED = 'APPROVED'  # -> C
    CANCELLED = 'CANCELLED'
    # MISSED = 'MISSED'
    # FINISHED = 'FINISHED'


class Visit(BM):
    status: str
    # cp
    version: Literal[1]
    phone: str
    client_id: str
    services: List[FServiceToVisit]



@app.post('/visit')
async def create_visit(visit: Visit):
    # how to prevent DDoS?
    return visit

@app.get('/visits')
async def get_visits():
    return [Visit(version=1, phone='375', client_id='123', services=[])]

@app.put('/visit/{visit_id}')
async def update_visit(visit_id: str, visit: Visit):
    return None

class Client(BM):
    name: str
    balance: float
    logo: str


async def root():
    return {'message': 'pong'}

# @app.post('/tests')
# async def create_test(t: T):
#     return t

class TimeSlot(BM):
    time_from: datetime.time
    time_to: datetime.time

class Day(BM):
    date: datetime.date
    timeslots: List[TimeSlot]

class DayTimeAvailability(BM):
    days: List[Day]

@app.get('/availability/{client_id}')
async def get_client_availability(
    # service_id = None,
    # worker_id = None,
    ) -> DayTimeAvailability:
    return DayTimeAvailability(
        days=[Day(
                date=datetime.date(year=2021, month=8, day=18),
                timeslots=[TimeSlot(
                    time_from=datetime.time(hour=15, minute=15),
                    time_to=datetime.time(hour=15, minute=15),
                )]
            )]
    )
    ...

class Worker(BM):
    id: str
    name: str

# @app.post('/worker_avaliability/{worker_id}')
# async def create_worker_availability()