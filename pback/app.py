import datetime
from datetime import timedelta
from enum import Enum
from io import BytesIO
from re import L
from typing import Literal, Optional, Iterator

import structlog
import uvicorn  # type: ignore
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions as exceptions
import crud
import db
import models
from schemas import InVisit, OutVisit, TokenOut, UserCreate, UserOut
from schemas.availability import (
    Availability,
    AvailabilityPerWorker,
    TimeSlotType,
    _get_client_availability,
)
from schemas.service import CreateService, OutService, OutServices
from schemas.slot import CreateSlot, CreateWeeklySlot, Slot
from schemas.worker import CreateWorker, OutWorker, OutWorkers, UpdateWorker
from utils.users import (
    get_current_user,
    get_current_user_or_none,
    jwtfy,
    validate_password,
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
@app.post("/signup", response_model=TokenOut)
async def create_user(
    user: UserCreate, s: Session = Depends(db.get_session)
) -> dict[str, str | int]:
    # print(user)
    # return {"access_token": 'asda', "token_type": "bearer"}

    db_user = crud.get_user_by_email(s, user.email)
    if db_user:
        raise exceptions.EmailExists
    db_user = crud.get_user_by_username(s, user.username)
    if db_user:
        raise exceptions.UsernameExists
    db_client = crud.create_client(s, user.company)
    db_user = crud.create_user(s, user, db_client.client_id)
    # TODO add to client created_by user
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt = jwtfy(access_token)
    return {
        "access_token": jwt,
        "token_type": "bearer",
        "client_id": db_client.client_id,
    }


@app.get("/users/me/", response_model=UserOut)
async def read_users_me(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    return current_user


@app.get("/my_user", response_model=UserOut)
async def read_users_me2(
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> Optional[models.User]:
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    s: Session = Depends(db.get_session),
) -> dict[Literal["access_token", "token_type"], str]:
    db_user = crud.get_user_by_username(s, form_data.username)
    if not db_user:
        raise exceptions.BadCreds
    hashed_password = db_user.hashed_password
    if not (validated := validate_password(form_data.password, hashed_password)):
        raise exceptions.BadCreds
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt_token = jwtfy(access_token)
    return {"access_token": jwt_token, "token_type": "bearer"}


# VISITS
@app.get("/visit/{visit_id}", response_model=OutVisit)
def get_visit(
    visit_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Visit:
    # return OutVisit.Example()
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

    def _list_services() -> Iterator[models.Service]:
        for service_wrapped in visit.services:
            service = crud.get_service(
                s,
                service_id=service_wrapped.service_id,
                not_found=exceptions.ServiceNotFound,
            )
            assert service is not None
            yield service

    services = list(_list_services())
    assert len(services) > 0

    slot = CreateSlot(
        name=f"Визит в {visit.from_dt}",
        slot_type=TimeSlotType.VISIT,
        client_id=visit.client_id,
        worker_id=visit.worker_id,
        from_datetime=visit.from_dt,
        to_datetime=visit.from_dt + timedelta(seconds=sum([service.seconds for service in services])),
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
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
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
    current_user: models.User = Depends(get_current_user),
) -> list[models.Visit]:
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


@app.put("/visit/{visit_id}")
async def update_visit(
    visit_id: str,
    visit: InVisit,
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> None:
    return None


@app.delete("/visit/{visit_id}")
async def delete_visit(visit_id: str) -> None:
    return None


# WORKERS
@app.post("/worker", response_model=OutWorker)
async def create_worker(
    worker: CreateWorker,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Worker:
    # TODO notify user that he needs to add company schedule
    # if worker.use_company_schedule:
    # wl = crud.get_client_weeklyslot(s, current_user.client_id)
    # if wl is None:
    # raise HTTPException(428, "Schedule needs to be created first")
    client_id = current_user.client_id
    db_worker = crud.create_worker(s, worker, client_id)
    return db_worker


@app.get("/worker/{worker_id}", response_model=OutWorker)
async def get_worker(
    worker_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


@app.put("/worker/{worker_id}", response_model=OutWorker)
async def update_worker(
    worker_id: int,
    worker: UpdateWorker,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, worker_id)
    return db_worker


@app.delete("/worker/{worker_id}")
async def delete_worker(worker_id: str) -> None:
    return None


@app.get("/client/{client_id}/workers", response_model=OutWorkers)
async def get_workers_by_client(
    client_id: int,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, client_id)

    return OutWorkers(workers=db_workers)


@app.get("/workers", response_model=OutWorkers)
async def get_workers(
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, current_user.client_id)

    return OutWorkers(workers=db_workers)


@app.post("/file")
async def create_file(
    file: UploadFile = File(...),
    s: Session = Depends(db.get_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> dict[Literal["file_id"], int]:
    # TODO check user
    db_file_id = crud.load_file(s, file, 5)
    return {"file_id": db_file_id}


@app.get("/file/{file_name}")
async def get_file(
    file_name: str,
    s: Session = Depends(db.get_session),
    # current_user: Optional[models.User] = Depends(get_current_user_or_none),
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
    # current_user: models.User = Depends(get_current_user),
) -> Availability:
    worker = crud.get_worker(s, worker_id)
    assert worker is not None

    total_service_length: Optional[int] = None
    if services:
        _services = [int(s) for s in services.split(",")]
        total_service_length = 0
        for service_id in _services:
            service = crud.get_service(
                s, service_id, not_found=exceptions.ServiceNotFound
            )
            assert service is not None
            assert service.seconds is not None  # this is strange, mad mypy
            total_service_length += service.seconds
    av = await Availability.GetWorkerAV(s, worker, service_length=total_service_length)
    return av


@app.get("/client/{client_id}/availability/", response_model=AvailabilityPerWorker)
async def get_client_availability(
    client_id: int,
    services: Optional[str] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(get_current_user),
) -> AvailabilityPerWorker:
    total_service_length = None
    if services:
        _services = [int(s) for s in services.split(",")]
        total_service_length = 0
        for service_id in _services:
            service = crud.get_service(
                s, service_id, not_found=exceptions.ServiceNotFound
            )
            assert service is not None
            assert service.seconds is not None  # this is strange, mad mypy
            total_service_length += service.seconds

    d = await _get_client_availability(client_id, total_service_length, s)
    return AvailabilityPerWorker.FromDict(d)


@app.post("/public_slot")
async def public_create_slot(
    slot: CreateSlot,
    s: Session = Depends(db.get_session),
) -> dict[Literal["slot_id"], int]:
    if slot.slot_type not in [TimeSlotType.VISIT]:
        raise exceptions.SlotType

    slot = await slot.visit_pick_worker_and_check(s, exc=exceptions.SlotNotAvailable)

    db_slot = crud.create_slot(s, slot)
    return {"slot_id": db_slot.slot_id}


@app.post("/slot")
async def create_slot(
    slot: CreateSlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> dict[Literal["slot_id"], int]:
    # TODO check against availability
    if slot.slot_type == TimeSlotType.VISIT:
        slot = await slot.visit_pick_worker_and_check(
            s, exc=exceptions.SlotNotAvailable
        )
    # for now I let availiability to duplicate
    db_slot = crud.create_slot(s, slot)
    return {"slot_id": db_slot.slot_id}


@app.delete("/slot/{slot_id}", response_model=Slot)
async def delete_client_slot(
    slot_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> Literal["OK"]:
    # check same client
    # check time being free
    db_slot = crud.get_slot(s, slot_id)
    if db_slot is None:
        crud.delete_slot(s, slot_id)
    return "OK"


@app.post("/client/{client_id}/client_weekly_slot")
async def create_client_weekly_slot(
    client_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> Literal["OK"]:
    assert client_id == current_user.client_id
    # check time being free ?
    # check another schedule being not present?
    db_slot = crud.create_weekly_slot(s, slot, client_id)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"


@app.post("/worker_weekly_slot/{worker_id}")
async def create_worker_weekly_slot(
    worker_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> Literal["OK"]:
    # check same client
    # check time being free
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker
    client_id = db_worker.client_id
    db_slot = crud.create_weekly_slot(s, slot, client_id, worker_id=worker_id)
    # print(db_slot.schedule_by_day)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"


@app.post("/service", response_model=OutService)
async def create_service(
    service: CreateService,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Service:
    client_id = current_user.client_id
    db_service = crud.create_service(s, service, client_id)
    return db_service


@app.get("/service/{service_id}", response_model=OutService)
async def get_service(
    service_id: int,
    s: Session = Depends(db.get_session),
) -> Optional[models.Service]:
    return crud.get_service(s, service_id)


@app.get("/client/{client_id}/service/{service_id}", response_model=OutService)
async def get_service_by_client(
    client_id: int,
    service_id: int,
    s: Session = Depends(db.get_session),
) -> Optional[models.Service]:
    return crud.get_service(s, service_id)


@app.get("/client/{client_id}/services", response_model=OutServices)
async def get_services_by_client(
    client_id: int,
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(get_current_user),
) -> OutServices:
    services = crud.get_services(s, client_id, worker_id=worker_id)
    return OutServices(services=services)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
