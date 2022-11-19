import datetime
import uuid
from datetime import timedelta
from typing import List, Optional, Union

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

import schemas
from features import users
from models import (
    Client,
    File,
    Service,
    Slot,
    Token,
    User,
    Visit,
    WeeklySlot,
    Worker,
    WorkersServices,
)


def get_visit(db: Session, visit_id: int) -> Optional[Visit]:
    return Visit.get_by_id(db, visit_id)


def get_visits(db: Session, client_id: int, worker_id: Optional[int] = None):
    q = db.query(Visit).filter(Visit.client_id == client_id)
    if worker_id:
        q = q.filter(Visit.worker_id)
    return q.all()


def create_visit(
    db: Session,
    visit: schemas.InVisit,
    *,
    customer_id: Optional[int] = None,
    slot_id: Optional[int] = None,
    worker_id: Optional[int] = None,
) -> Visit:
    db_visit = Visit(
        client_id=visit.client_id,
        customer_id=customer_id,
        email=visit.email,
        has_notification=visit.remind_me,
        phone=visit.phone,
        status="submitted",
        services=[s.service_id for s in visit.services],
        slot_id=slot_id,
        worker_id=visit.worker_id or worker_id,
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)  # why refresh?
    return db_visit


def create_client(db: Session, name: str) -> Client:
    db_client = Client(name=name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def create_user(db: Session, user: users.UserCreate, client_id: int) -> User:
    salt = users.make_salt()
    hashed_password = users.hash_password(user.password, salt)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        client_id=client_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_user_id(db: Session, user_id: Union[int, str]) -> Optional[User]:
    user_id = int(user_id)
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_token_id(db: Session, token_id: str) -> Optional[User]:
    t = db.query(Token).filter(Token.token_id == int(token_id)).first()
    if t is None or t.expires < datetime.datetime.now():
        return None

    assert t is not None
    user_id = t.user_id
    assert user_id is not None
    return get_user_by_user_id(db, user_id)


def create_user_token(db: Session, user_id: int) -> Token:
    token = Token(
        access_token=str(uuid.uuid4()),
        expires=datetime.datetime.now() + timedelta(weeks=4),
        user_id=user_id,
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def load_file(db: Session, file: UploadFile, client_id: int) -> int:
    db_file = File(
        client_id=client_id, file=file.file.read(), content_type=file.content_type
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.file_id


def read_file(db: Session, file_id: int) -> Optional[File]:
    return File.get_by_id(db, file_id)


def get_worker(db: Session, worker_id: int) -> Optional[Worker]:
    return Worker.get_by_id(db, worker_id)


def get_workers(db: Session, client_id: int) -> List[Worker]:
    return db.query(Worker).filter(Worker.client_id == client_id).all()


def create_worker(db: Session, worker: schemas.CreateWorker, client_id: int) -> Worker:
    w = worker
    db_worker = Worker(
        name=w.name,
        job_title=w.job_title,
        client_id=client_id,
        use_company_schedule=w.use_company_schedule
        if w.use_company_schedule is not None
        else True,
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def update_worker(db: Session, worker: schemas.UpdateWorker, worker_id: int) -> Worker:
    db_worker = get_worker(db, worker_id)
    assert db_worker is not None
    update = worker.dict()
    for field, value in update.items():
        if value is None:
            continue
        setattr(db_worker, field, value)
    db.commit()  # enough??
    return db_worker


def get_slot(db: Session, slot_id: int) -> Optional[Slot]:
    return Slot.get_by_id(db, slot_id)


def create_slot(db: Session, slot: schemas.CreateSlot) -> Slot:
    d = slot.dict()

    db_slot = Slot(**d)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def update_slot(db: Session, slot: schemas.UpdateSlot, slot_id: int) -> Slot:
    db_slot = get_slot(db, slot_id)
    assert db_slot is not None
    update = slot.dict()
    for field, value in update.items():
        if value is None:
            continue
        setattr(db_slot, field, value)
    db.commit()  # enough??
    return db_slot


def delete_slot(db: Session, slot_id: int) -> None:
    db.query(Slot).filter(Slot.slot_id == slot_id).delete()


def get_client_slots(
    db: Session, client_id: int, *, slot_types: Optional[List[str]]
) -> List[Slot]:
    # add filtering
    q = db.query(Slot).filter(Slot.client_id == client_id)
    if slot_types:
        q = q.filter(Slot.slot_type.in_(slot_types))
    return q.all()


def get_client_weeklyslot(db: Session, client_id: int) -> Optional[WeeklySlot]:
    # add filtering
    return (
        db.query(WeeklySlot)
        .filter(WeeklySlot.client_id == client_id, WeeklySlot.worker_id == None)
        .first()
    )


def get_worker_weeklyslot(db: Session, worker_id: int) -> Optional[WeeklySlot]:
    # add filtering
    return db.query(WeeklySlot).filter(WeeklySlot.worker_id == worker_id).first()


def get_worker_slots(
    db: Session, worker_id: int, *, slot_types: Optional[List[str]]
) -> List[Slot]:
    # add filtering
    q = db.query(Slot).filter(Slot.worker_id == worker_id)
    if slot_types:
        q = q.filter(Slot.slot_type.in_(slot_types))
    return q.all()


def create_weekly_slot(
    db: Session,
    slot: schemas.CreateWeeklySlot,
    client_id: int,
    *,
    worker_id: Optional[int] = None,
) -> WeeklySlot:
    schedule = slot.dict()
    db_slot = WeeklySlot(
        client_id=client_id, schedule_by_day=schedule, worker_id=worker_id
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def create_service(
    db: Session,
    service: schemas.CreateService,
    client_id: int,
) -> Service:
    serv = service.dict()
    db_service = Service(**serv, client_id=client_id)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_service(
    db: Session, service_id: int, *, not_found: Optional[HTTPException] = None
) -> Optional[Service]:
    q = db.query(Service).filter(Service.service_id == service_id)
    slot = q.first()
    if not slot and not_found:
        raise not_found
    return slot


def get_services(
    db: Session, client_id: int, *, worker_id: Optional[int] = None
) -> List[Service]:
    if worker_id:
        return _get_services_for_worker(db, client_id, worker_id)
    return _get_services_for_client(db, client_id)


def _get_services_for_client(db: Session, client_id: int) -> List[Service]:
    q = db.query(Service).filter(Service.client_id == client_id)
    return q.all()


def _get_services_for_worker(
    db: Session, client_id: int, worker_id: int
) -> List[Service]:
    worker_services = db.query(WorkersServices).filter(
        WorkersServices.worker_id == worker_id
    )
    q = db.query(Service).filter(Service.service_id.in_(worker_services))  # todo: test
    return q.all()
