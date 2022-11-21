import datetime
from datetime import timedelta
from enum import Enum
from io import BytesIO
from typing import Iterator, Literal, Optional

import structlog
import uvicorn  # type: ignore
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions as exceptions
import crud
import db
import models
from features import services, slots, users, workers
from schemas.availability import (
    Availability,
    AvailabilityPerWorker,
    TimeSlotType,
    _get_client_availability,
)
from schemas.visit import InVisit, OutVisit

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


# VISITS
@app.get("/visit/{visit_id}", response_model=OutVisit)
def get_visit(
    visit_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Visit:
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise exceptions.VisitNotFound
    return visit


@app.post("/public_visit", response_model=OutVisit)
async def public_create_visit(
    visit: InVisit,
    s: Session = Depends(db.get_session),
    # TODO: visitor
) -> models.Visit:
    if visit.from_dt < datetime.datetime.now():
        raise exceptions.SlotNotAvailable

    services = crud.get_services_by_ids(s, [s.service_id for s in visit.services])
    assert len(services) > 0
    visit_len_seconds: int = sum([service.seconds for service in services])

    slot = slots.CreateSlot(
        name=f"Визит в {visit.from_dt}",
        slot_type=TimeSlotType.VISIT,
        client_id=visit.client_id,
        worker_id=visit.worker_id,
        from_datetime=visit.from_dt,
        to_datetime=visit.from_dt + timedelta(seconds=visit_len_seconds),
    )
    slot = await slot.visit_pick_worker_and_check(s, exc=exceptions.SlotNotAvailable)

    db_slot = crud.create_slot(s, slot)

    db_visit = crud.create_visit(
        s,
        visit,
        slot_id=db_slot.slot_id,
        worker_id=db_slot.worker_id,
        customer_id=None,
    )
    return db_visit


@app.post("/visit", response_model=OutVisit)
def create_visit(
    visit: InVisit,
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> models.Visit:
    db_visit = crud.create_visit(s, visit)
    return db_visit


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


@app.get("/visits")
async def get_visits(
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> list[models.Visit]:
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


@app.put("/visit/{visit_id}")
async def update_visit(
    visit_id: str,
    visit: InVisit,
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> None:
    return None


@app.delete("/visit/{visit_id}")
async def delete_visit(visit_id: str) -> None:
    return None


@app.post("/file")
async def create_file(
    file: UploadFile = File(...),
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> dict[Literal["file_id"], int]:
    # TODO check user
    db_file_id = crud.load_file(s, file, 5)
    return {"file_id": db_file_id}


@app.get("/file/{file_name}")
async def get_file(
    file_name: str,
    s: Session = Depends(db.get_session),
    # current_user: Optional[models.User] = Depends(users.get_current_user_or_none),
) -> StreamingResponse:
    f = crud.read_file(s, int(file_name))
    assert f is not None
    # print("File id:", f.file_id)
    b = f.file
    bytes_io = BytesIO()
    bytes_io.write(b)
    bytes_io.seek(0)
    r = StreamingResponse(bytes_io, media_type=f.content_type)
    return r


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
