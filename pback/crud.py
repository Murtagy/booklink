import datetime
import uuid
from datetime import timedelta
from typing import List, Optional, Union

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlmodel import col, delete, select

from features import services, slots, users, visits
from features.workers import schemas as workers
from models import (
    Client,
    File,
    Service,
    Skill,
    Slot,
    Token,
    User,
    Visit,
    WeeklySlot,
    Worker,
)


def get_visit(db: Session, visit_id: int) -> Optional[Visit]:
    stmt = select(Visit).where(Visit.visit_id == visit_id)
    return db.execute(stmt).scalar_one_or_none()


def get_visits(db: Session, client_id: int, worker_id: Optional[int] = None):
    q = select(Visit).where(Visit.client_id == client_id)
    if worker_id:
        q = q.where(Visit.worker_id == worker_id)
    return db.execute(q).scalars().all()


def create_visit(
    db: Session,
    *,
    client_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    slot_id: Optional[int] = None,
    worker_id: Optional[int] = None,
) -> Visit:
    db_visit = Visit(
        client_id=client_id,
        customer_id=customer_id,
        has_notification=False,
        status="submitted",
        # services=[s.service_id for s in visit.services],
        slot_id=slot_id,
        worker_id=worker_id,
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def create_customer_visit(
    db: Session,
    visit: visits.InVisit,
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
    stmt = select(User).where(User.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_token_id(db: Session, token_id: str) -> Optional[User]:
    stmt = select(Token).where(Token.token_id == int(token_id))
    t = db.execute(stmt).scalar_one_or_none()
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
    db_file = File(client_id=client_id, file=file.file.read(), content_type=file.content_type)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.file_id


def read_file(db: Session, file_id: int) -> Optional[File]:
    stmt = select(File).where(File.file_id == file_id)
    return db.execute(stmt).scalars().one_or_none()


def get_worker(db: Session, worker_id: int) -> Optional[Worker]:
    stmt = select(Worker).where(Worker.worker_id == worker_id)
    return db.execute(stmt).scalars().one_or_none()


def get_workers(db: Session, client_id: int) -> List[Worker]:
    stmt = select(Worker).where(Worker.client_id == client_id)
    return db.execute(stmt).scalars().all()


def create_worker(db: Session, worker: workers.CreateWorker, client_id: int) -> Worker:
    w = worker
    db_worker = Worker(
        name=w.name,
        job_title=w.job_title,
        client_id=client_id,
        use_company_schedule=w.use_company_schedule if w.use_company_schedule is not None else True,
    )
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def update_worker(db: Session, worker: workers.UpdateWorker, worker_id: int) -> Worker:
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
    stmt = select(Slot).where(Slot.slot_id == slot_id)
    return db.execute(stmt).scalars().one_or_none()


def create_slot(db: Session, slot: slots.CreateSlot) -> Slot:
    d = slot.dict()

    db_slot = Slot(**d)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def update_slot(db: Session, slot: slots.UpdateSlot, slot_id: int) -> Slot:
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
    stmt = delete(Slot.__tablename__).where(Slot.slot_id == slot_id)
    db.execute(stmt)
    return


def get_client_slots(db: Session, client_id: int, *, slot_types: Optional[List[str]]) -> List[Slot]:
    # add filtering
    q = select(Slot).where(Slot.client_id == client_id)
    if slot_types:
        q = q.where(col(Slot.slot_type).in_(slot_types))
    return db.execute(q).scalars().all()


def get_client_weeklyslot(db: Session, client_id: int) -> Optional[WeeklySlot]:
    # add filtering
    stmt = (
        select(WeeklySlot)
        .where(WeeklySlot.client_id == client_id)
        .where(WeeklySlot.worker_id == None)
    )
    return db.execute(stmt).scalar_one_or_none()


def get_worker_weeklyslot(db: Session, worker_id: int) -> Optional[WeeklySlot]:
    # add filtering
    stmt = select(WeeklySlot).where(WeeklySlot.worker_id == worker_id)
    return db.execute(stmt).scalar_one_or_none()


def get_worker_slots(db: Session, worker_id: int, *, slot_types: Optional[List[str]]) -> List[Slot]:
    # add filtering
    q = select(Slot).where(Slot.worker_id == worker_id)
    if slot_types:
        q = q.where(col(Slot.slot_type).in_(slot_types))
    return db.execute(q).scalars().all()


def create_weekly_slot(
    db: Session,
    slot: slots.CreateWeeklySlot,
    client_id: int,
    *,
    worker_id: Optional[int] = None,
) -> WeeklySlot:
    schedule = slot.dict()
    db_slot = WeeklySlot(client_id=client_id, schedule_by_day=schedule, worker_id=worker_id)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def create_service(
    db: Session,
    service: services.CreateService,
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
    q = select(Service).where(Service.service_id == service_id)
    service = db.execute(q).scalar_one_or_none()
    if not service and not_found:
        raise not_found
    return service


def get_services_by_ids(
    db: Session, service_ids: list[int], *, not_found: Optional[HTTPException] = None
) -> list[Service]:
    q = select(Service).where(col(Service.service_id).in_(service_ids))
    services = db.execute(q).scalars().all()
    if not services and not_found:
        raise not_found
    return services


def get_services(db: Session, client_id: int, *, worker_id: Optional[int] = None) -> List[Service]:
    if worker_id:
        return _get_worker_skills(db, worker_id)
    return _get_services_for_client(db, client_id)


def create_skill(db: Session, worker_id: int, service_id: int) -> None:
    db.add(Skill(worker_id=worker_id, service_id=service_id))
    db.commit()
    return


def delete_skill(db: Session, worker_id: int, service_id: int) -> None:
    db.execute(
        delete(Skill.__tablename__)
        .where(Skill.worker_id == worker_id)
        .where(Skill.service_id == service_id)
    )


def get_skill(db: Session, worker_id: int, service_id: int) -> Skill | None:
    q = select(Skill).where(Skill.worker_id == worker_id).where(Skill.service_id == service_id)
    r = db.execute(q).scalars().all()
    assert len(r) < 2
    return r[0] if r else None


def _get_services_for_client(db: Session, client_id: int) -> List[Service]:
    q = select(Service).where(Service.client_id == client_id)
    return db.execute(q).scalars().all()


def _get_worker_skills(db: Session, worker_id: int) -> List[Service]:
    skills_ids = select(Skill.service_id).where(Skill.worker_id == worker_id)
    q = select(Service).where(col(Service.service_id).in_(skills_ids))  # todo: test
    return db.execute(q).scalars().all()
