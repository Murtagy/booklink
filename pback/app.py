from enum import Enum
from typing import Optional

import structlog
import uvicorn  # type: ignore
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import files, services, slots, users, visits, workers
from schemas.availability import (
    Availability,
    AvailabilityPerWorker,
    _get_client_availability,
)

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3333",
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db.BaseModel.metadata.create_all(bind=db.engine)
logger = structlog.get_logger()


class StrEnum(str, Enum):
    ...


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


# USERS
app.post("/signup", response_model=users.TokenOut)(users.create_user_endpoint)
app.get("/users/me/", response_model=users.UserOut)(users.read_users_me_endpoint)
app.get("/my_user", response_model=users.UserOut)(users.read_users_me2_endpoint)
app.post("/token")(users.login_for_access_token_endpoint)

# WORKERS
app.get("/worker/{worker_id}", response_model=workers.OutWorker)(
    workers.get_worker_endpoint
)
app.put("/worker/{worker_id}", response_model=workers.OutWorker)(
    workers.update_worker_endpoint
)
app.delete("/worker/{worker_id}")(workers.delete_worker_endpoint)
app.get("/client/{client_id}/workers", response_model=workers.OutWorkers)(
    workers.get_workers_by_client_endpoint
)
app.get("/workers", response_model=workers.OutWorkers)(workers.get_workers_endpoint)
app.post("/worker", response_model=workers.OutWorker)(workers.create_worker_endpoint)

# SERVICES
app.post("/service", response_model=services.OutService)(
    services.create_service_endpoint
)
app.get("/service/{service_id}", response_model=services.OutService)(
    services.get_service_endpoint
)
app.get("/client/{client_id}/service/{service_id}", response_model=services.OutService)(
    services.get_service_by_client_endpoint
)
app.get("/client/{client_id}/services", response_model=services.OutServices)(
    services.get_services_by_client_endpoint
)


@app.get("/public_avaliability")
async def get_avaliability(
    client_id: int,
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    # TODO Visitor
) -> list[models.Visit]:
    # schedule =
    # slots    =
    visits = crud.get_visits(s, client_id, worker_id=worker_id)

    # schedule - slots - visits = avalibility : List[Slots]
    return visits


# VISITS
app.get("/visit/{visit_id}", response_model=visits.OutVisit)(visits.get_visit_endpoint)
app.post("/public_visit", response_model=visits.OutVisit)(
    visits.public_create_visit_endpoint
)
app.get("/visits")(visits.get_visits_endpoint)
app.post("/visit", response_model=visits.OutVisit)(visits.create_visit_endpoint)
app.put("/visit/{visit_id}")(visits.update_visit_endpoint)
# @app.delete("/visit/{visit_id}")
# async def delete_visit(visit_id: str) -> None:
# return None


app.post("/file")(files.create_file_endpoint)
app.get("/file/{file_name}")(files.get_file_endpoint)


@app.get(
    "/client/{client_id}/worker/{worker_id}/availability", response_model=Availability
)
async def get_worker_availability(
    worker_id: int,
    services: Optional[str] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> Availability:
    worker = crud.get_worker(s, worker_id)
    assert worker is not None

    total_service_length: Optional[int] = None
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        total_service_length = sum([s.seconds for s in db_services])
    av = await Availability.GetWorkerAV(s, worker, service_length=total_service_length)
    return av


@app.get("/client/{client_id}/availability/", response_model=AvailabilityPerWorker)
async def get_client_availability(
    client_id: int,
    services: Optional[str] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> AvailabilityPerWorker:
    total_service_length = None
    if services:
        service_ids = [int(s) for s in services.split(",")]
        db_services = crud.get_services_by_ids(s, service_ids)
        total_service_length = sum([s.seconds for s in db_services])

    d = await _get_client_availability(client_id, total_service_length, s)
    return AvailabilityPerWorker.FromDict(d)


app.post("/public_slot")(slots.public_create_slot_endpoint)
app.post("/slot")(slots.create_slot_endpoint)
app.delete("/slot/{slot_id}", response_model=slots.Slot)(
    slots.delete_client_slot_endpoint
)
app.post("/client/{client_id}/client_weekly_slot")(
    slots.create_client_weekly_slot_endpoint
)
app.post("/worker_weekly_slot/{worker_id}")(slots.create_worker_weekly_slot_endpoint)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
