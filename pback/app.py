# TODO: SPA или не нужен вью для большинства
import datetime
from enum import Enum
from typing import List, Literal

from fastapi import Depends, FastAPI
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session

import crud
import db
import models
from schemas.visit import InVisit, OutVisit, Visit
from schemas.worker import InWorker, OutWorker

app = FastAPI()
models.BaseModel.metadata.create_all(bind=db.engine)

# Dependency
def get_db_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


class StrEnum(str, Enum):
    ...


@app.get("/ping")
async def ping():
    return {"message": "pong"}


# VISITS
@app.get("/visit/{visit_id}")
def get_visit(visit_id: str, s: Session = Depends(get_db_session)) -> OutVisit:
    # return OutVisit.Example()
    return crud.get_visit(s, visit_id)


@app.post("/visit")
async def create_visit(visit: InVisit) -> OutVisit:
    # how to prevent DDoS?
    return visit


@app.get("/visits")
async def get_visits():
    return [OutVisit.Example()]


@app.put("/visit/{visit_id}")
async def update_visit(visit_id: str, visit: InVisit):
    return None


@app.delete("/visit/{visit_id}")
async def delete_visit(visit_id: str):
    return True


# WORKERS
@app.post("/worker")
async def create_worker(worker: InWorker) -> OutWorker:
    return worker


@app.get("/worker/{worker_id}")
async def get_worker(worker_id: str) -> OutWorker:
    return OutWorker


@app.put("/worker/{worker_id}")
async def update_worker(worker: InWorker) -> OutWorker:
    return OutWorker(id="11", name="Alfa Romeo", job_title="Инженер")


@app.delete("/worker/{worker_id}")
async def delete_worker(worker_id: str):
    return True


class TimeSlot(BM):
    time_from: datetime.time
    time_to: datetime.time


class Day(BM):
    date: datetime.date
    timeslots: List[TimeSlot]


class DayTimeAvailability(BM):
    days: List[Day]


@app.get("/availability/{client_id}")
async def get_client_availability(
    # service_id = None,
    # worker_id = None,
) -> DayTimeAvailability:
    return DayTimeAvailability(
        days=[
            Day(
                date=datetime.date(year=2021, month=8, day=18),
                timeslots=[
                    TimeSlot(
                        time_from=datetime.time(hour=15, minute=15),
                        time_to=datetime.time(hour=15, minute=30),
                    )
                ],
            )
        ]
    )
    ...


# @app.post('/worker_avaliability/{worker_id}')
# async def create_worker_availability()
