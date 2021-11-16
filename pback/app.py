import json
from enum import Enum
from io import BytesIO
from typing import Any, Dict, List, Literal, Optional

import structlog
import uvicorn  # type: ignore
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from schemas import InVisit, OutVisit, TokenOut, UserCreate, UserOut
from schemas.availability import Availability, TimeSlotType
from schemas.slot import CreateSlot, CreateWeeklySlot, Slot, WeeklySlot
from schemas.worker import CreateWorker, OutWorker, UpdateWorker
from utils.users import oauth, validate_password

SECRET_KEY = "12325e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.BaseModel.metadata.create_all(bind=db.engine)
logger = structlog.get_logger()

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
def jwtfy(token: models.Token):
    return jwt.encode({"sub": str(token.token_id)}, SECRET_KEY, algorithm=ALGORITHM)


def unjwttfy_token_id(token: Optional[str]) -> Optional[str]:
    if token is None:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get("sub")


@app.post("/signup", response_model=TokenOut)
async def create_user(user: UserCreate, s: Session = Depends(get_db_session)):
    print(user)
    # return {"access_token": 'asda', "token_type": "bearer"}

    db_user = crud.get_user_by_email(s, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User email already exists")
    db_user = crud.get_user_by_username(s, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_client = crud.create_client(s, user.company)
    db_user = crud.create_user(s, user, db_client.client_id)
    # TODO add to client created_by user
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt = jwtfy(access_token)
    return {"access_token": jwt, "token_type": "bearer"}


async def get_current_user_or_none(
    token: Optional[str] = Depends(oauth), s: Session = Depends(get_db_session)
) -> Optional[models.User]:
    if token:
        print("TOKEN")
        return await get_current_user(token, s)
    else:
        print("NO TOKEN")
        return None


BadTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad token!!!",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: Optional[str] = Depends(oauth), s: Session = Depends(get_db_session)
) -> models.User:
    try:
        token_id = unjwttfy_token_id(token)
        if token_id is None:
            raise BadTokenException
    except JWTError:
        raise BadTokenException
    user = crud.get_user_by_token_id(s, token_id=token_id)
    if user is None:
        raise BadTokenException
    return user


@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/my_user", response_model=UserOut)
async def read_users_me2(
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
):
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    s: Session = Depends(get_db_session),
):
    db_user = crud.get_user_by_username(s, form_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = db_user.hashed_password
    if validate_password(form_data.password, hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = crud.create_user_token(s, db_user.user_id)
    jwt_token = jwtfy(access_token)
    return {"access_token": jwt_token, "token_type": "bearer"}


# VISITS
@app.get("/visit/{visit_id}", response_model=OutVisit)
def get_visit(
    visit_id: int,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
) -> models.Visit:
    # return OutVisit.Example()
    visit = crud.get_visit(s, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@app.post("/public_visit", response_model=OutVisit)
def public_create_visit(
    visit: InVisit,
    s: Session = Depends(get_db_session),
    # TODO: visitor
) -> models.Visit:
    db_visit = crud.create_visit(s, visit)
    return db_visit


@app.post("/visit", response_model=OutVisit)
def create_visit(
    visit: InVisit,
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> models.Visit:
    db_visit = crud.create_visit(s, visit)
    return db_visit


@app.get("/public_avaliability")
async def get_avaliability(
    client_id: int,
    worker_id: Optional[int] = None,
    s: Session = Depends(get_db_session),
    # TODO Visitor
):
    # schedule =
    # slots    =
    visits = crud.get_visits(s, client_id, worker_id=worker_id)

    # schedule - slots - visits = avalibility : List[Slots]
    return visits


@app.get("/visits")
async def get_visits(
    worker_id: Optional[int] = None,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    client_id = current_user.client_id

    return crud.get_visits(s, client_id, worker_id=worker_id)


@app.put("/visit/{visit_id}")
async def update_visit(
    visit_id: str,
    visit: InVisit,
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
):
    return None


@app.delete("/visit/{visit_id}")
async def delete_visit(visit_id: str):
    return True


# WORKERS
@app.post("/worker", response_model=OutWorker)
async def create_worker(
    worker: CreateWorker,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    client_id = current_user.client_id
    db_worker = crud.create_worker(s, worker, client_id)
    return db_worker


@app.get("/worker/{worker_id}", response_model=OutWorker)
async def get_worker(
    worker_id: int,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


@app.put("/worker/{worker_id}", response_model=OutWorker)
async def update_worker(
    worker_id: int,
    worker: UpdateWorker,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, worker_id)
    return db_worker


@app.delete("/worker/{worker_id}")
async def delete_worker(worker_id: str):
    return True


@app.post("/file")
async def create_file(
    file: UploadFile = File(...),
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
):
    # TODO check user
    db_file_id = crud.load_file(s, file, 5)
    return {"file_id": db_file_id}


@app.get("/file/{file_name}")
async def get_file(
    file_name: str,
    s: Session = Depends(get_db_session),
    # current_user: Optional[models.User] = Depends(get_current_user_or_none),
) -> StreamingResponse:
    f = crud.read_file(s, int(file_name))
    assert f is not None
    print("File id:", f.file_id)
    b = f.file
    bytes_io = BytesIO()
    bytes_io.write(b)
    bytes_io.seek(0)
    r = StreamingResponse(bytes_io, media_type=f.content_type)
    return r


@app.get("/worker_availability/{worker_id}")
async def get_worker_availability(
    worker_id=None,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
) -> Availability:
    worker = crud.get_worker(s, worker_id)
    assert worker is not None
    uses_company_schedule = worker.use_company_schedule
    if uses_company_schedule:
        company_schedule = crud.get_client_weeklyslot(s, worker.client_id)
    # NOT DONE
    assert company_schedule
    assert isinstance(company_schedule.schedule_by_day, dict)
    return Availability.CreateFromSchedule(company_schedule.schedule_by_day)


@app.get("/client_availability/{client_id}")
async def get_client_availability(
    client_id: int,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
) -> Availability:
    # weekly_slots = crud.get_client_weeklyslot(s, client_id)
    # assert weekly_slots
    # assert isinstance(weekly_slots.schedule_by_day, dict)
    workers = crud.get_workers(s, client_id)
    worker_avs: List[Availability] = []
    for worker in workers:
        if worker.use_company_schedule:
            wl = crud.get_client_weeklyslot(s, worker.client_id)
            assert wl
            assert isinstance(wl.schedule_by_day, dict)
            av = Availability.CreateFromSchedule(wl.schedule_by_day)
        else:
            wl = crud.get_worker_weeklyslot(s, worker.worker_id)
            if wl is not None:
                assert isinstance(wl.schedule_by_day, dict)
                av = Availability.CreateFromSchedule(wl.schedule_by_day)
            else:
                slots = crud.get_worker_slots(
                    s, worker_id=worker.worker_id, slot_types=[TimeSlotType.AVAILABLE]
                )
                av = Availability.CreateFromSlots(slots)

        busy_slots = crud.get_worker_slots(
            s, worker.worker_id, slot_types=["busy", "visit"]
        )
        av.ReduceAvailabilityBySlots(busy_slots)
        # TODO SPLIT BY SERVICE SELECTED LENGTH
        av.SplitByLength(length_seconds=45 * 60)
        worker_avs.append(av)

    av = Availability.WorkersToClient(worker_avs)
    return av


@app.post("/worker_slot/{worker_id}")
async def create_worker_slot(
    worker_id: int,
    slot: CreateSlot,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    # check same client
    # check time being free
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker
    client_id = db_worker.client_id
    db_slot = crud.create_slot(s, slot, client_id, worker_id=worker_id)
    return db_slot


@app.post("/client_slot/{client_id}", response_model=Slot)
async def create_client_slot(
    client_id: int,
    slot: CreateSlot,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    # check same client
    # check time being free
    db_slot = crud.create_slot(s, slot, client_id)
    return db_slot


@app.delete("/slot/{slot_id}", response_model=Slot)
async def delete_client_slot(
    slot_id: int,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    # check same client
    # check time being free
    db_slot = crud.get_slot(s, slot_id)
    crud.delete_slot(s, slot_id)
    return db_slot


@app.post("/client_weekly_slot/{client_id}")
async def create_client_weekly_slot(
    client_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    # check same client
    # check time being free
    db_slot = crud.create_weekly_slot(s, slot, client_id)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"


@app.post("/worker_weekly_slot/{worker_id}")
async def create_worker_weekly_slot(
    worker_id: int,
    slot: CreateWeeklySlot,
    s: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    # check same client
    # check time being free
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker
    client_id = db_worker.client_id
    db_slot = crud.create_weekly_slot(s, slot, client_id, worker_id=worker_id)
    print(db_slot.schedule_by_day)
    # d = {"slot_id": db_slot.slot_id, **db_slot.schedule_by_day}
    return "OK"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
