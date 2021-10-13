# TODO: SPA или не нужен вью для большинства
import datetime
from enum import Enum
from io import BytesIO
from typing import List, Literal, Optional

import structlog
from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse, StreamingResponse
from jose import JWTError, jwt  # type: ignore
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from schemas import InVisit, OutVisit, TokenOut, UserCreate, UserOut
from schemas.worker import InWorker, OutWorker
from utils.users import oauth, validate_password

SECRET_KEY = "12325e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
app = FastAPI()
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
    db_user = crud.get_user_by_email(s, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User email already exists")
    db_user = crud.get_user_by_username(s, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = crud.create_user(s, user)
    access_token = crud.create_user_token(s, db_user.user_id)
    jwt = jwtfy(access_token)
    return {"access_token": jwt, "token_type": "bearer"}


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Bad token!!!",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user_or_none(
    token: Optional[str] = Depends(oauth), s: Session = Depends(get_db_session)
) -> Optional[models.User]:
    if token:
        print('TOKEN')
        return await get_current_user(token, s)
    else:
        print('NO TOKEN')
        return None


async def get_current_user(
    token: Optional[str] = Depends(oauth), s: Session = Depends(get_db_session)
) -> models.User:
    try:
        token_id = unjwttfy_token_id(token)
        if token_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_token_id(s, token_id=token_id)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_us  er: User = Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/users/me2/", response_model=UserOut)
async def read_users_me(current_user: Optional[models.User] = Depends(get_current_user_or_none)):
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


@app.post("/visit", response_model=OutVisit)
def create_visit(
    visit: InVisit, 
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none)
) -> models.Visit:
    db_visit = crud.create_visit(s, visit)
    return db_visit


@app.get("/visits")
async def get_visits(
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none)
):
    return [OutVisit.Example()]


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


@app.post("/file")
async def create_file(
    file: UploadFile = File(...),
    s: Session = Depends(get_db_session),
    current_user: Optional[models.User] = Depends(get_current_user_or_none),
 ):
    # TODO check user
    db_file_id = crud.load_file(s, file, 5)
    return {"file_id": db_file_id}

@app.get("/files/{file_name}")
async def create_file(
    file_name: str,
    s: Session = Depends(get_db_session),
    # current_user: Optional[models.User] = Depends(get_current_user_or_none),
 ) -> StreamingResponse:
    f = crud.read_file(s, int(file_name))
    print('File id:', f.file_id)
    b = f.file
    bytes_io = BytesIO()
    bytes_io.write(b)
    bytes_io.seek(0)
    r = StreamingResponse(bytes_io, media_type=f.content_type)
    return r
    

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
