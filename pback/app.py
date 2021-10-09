# TODO: SPA или не нужен вью для большинства
import datetime
from enum import Enum
from typing import List, Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from schemas import InVisit, OutVisit, UserCreate, UserOut
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


# USERS
@app.post("/signup", response_model=UserOut)
def create_user(user: UserCreate, s: Session = Depends(get_db_session)) -> models.User:
    db_user = crud.create_user(s, user)
    return db_user


# VISITS
@app.get("/visit/{visit_id}", response_model=OutVisit)
def get_visit(visit_id: int, s: Session = Depends(get_db_session)) -> models.Visit:
    # return OutVisit.Example()
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@app.post("/visit", response_model=OutVisit)
def create_visit(visit: InVisit, s: Session = Depends(get_db_session)) -> models.Visit:
    db_visit = crud.create_visit(s, visit)
    return db_visit


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
async def create_worker(worker: InWorker) -> InWorker:
    return worker


# @app.get("/worker/{worker_id}")
# async def get_worker(worker_id: str) -> OutWorker:
#     return OutWorker


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
