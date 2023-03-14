from fastapi import Depends, Path, Query
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

from .. import app_exceptions, crud, db, models
from ..app_exceptions import WorkerNotFound
from . import services, skills, users


class CreateWorker(BM):
    name: str
    job_title: str


class UpdateWorker(BM):
    # worker_id: int
    name: None | str
    job_title: None | str


class OutWorker(BM):
    client_id: str
    worker_id: str
    name: str
    job_title: str

    class Config:
        orm_mode = True


class OutWorkers(BM):
    workers: list[OutWorker]


class SkillIn(BM):
    worker_id: int
    service_id: int
    picked: bool = True


class SkillsIn(BM):
    skills: list[SkillIn]


class Received(BM):
    msg: str = "Received"


def get_worker(
    worker_id: str = Path(regex=r"\d+"),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> OutWorker:
    db_worker = crud.get_worker(s, int(worker_id))
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return OutWorker.from_orm(db_worker)


def get_skilled_workers(
    s: Session,
    client_id: int,
    services: list[int],
):
    return [OutWorker.from_orm(w) for w in crud.get_skilled_workers(s, client_id, services)]

def get_worker_by_id(
    worker_id: int,
    s: Session,
) -> OutWorker:
    db_worker = crud.get_worker(s, int(worker_id))
    if not db_worker:
        raise WorkerNotFound
    return OutWorker.from_orm(db_worker)


def update_worker(
    worker: UpdateWorker,
    worker_id: str = Path(regex=r"\d+"),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, int(worker_id))
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, int(worker_id))
    return db_worker


def delete_worker(
    worker_id: str = Path(regex=r"\d+"),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> None:
    worker = crud.get_worker(s, int(worker_id))
    if not worker:
        raise WorkerNotFound
    worker.assure_id(current_user.client_id)
    crud.delete_worker(s, int(worker_id))
    return None


def get_workers_by_client(
    client_id: int,
    services: str | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, client_id)
    if services:
        services_ids = list(map(int, services.split(",")))
        return OutWorkers(
            workers=get_skilled_workers(s, client_id, services_ids)
        )

    return OutWorkers(workers=db_workers)


def get_workers(
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, current_user.client_id)

    return OutWorkers(workers=db_workers)


def create_worker(
    worker: CreateWorker,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    client_id = current_user.client_id
    db_worker = crud.create_worker(s, worker, client_id)
    return db_worker


def assure_worker_and_owner(s: Session, user: models.User, worker_id: int | str) -> None:
    worker = crud.get_worker(s, int(worker_id))
    if worker is None:
        raise WorkerNotFound
    if worker.client_id != user.client_id:
        raise ValueError


def _skill_picked(s: Session, worker_id: int, service_id: int) -> bool:
    ws = crud.get_skill(s, worker_id, service_id)
    if ws is None:
        return False
    else:
        return True


# endpoints:
def add_skill(
    skill: SkillIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Received:
    worker_id = skill.worker_id
    service_id = skill.service_id

    db_worker = crud.get_worker(s, worker_id)
    service = services.get_service_optional(service_id, s)

    if db_worker is None:
        raise WorkerNotFound
    if service is None:
        raise app_exceptions.ServiceNotFound

    assert current_user.client_id == db_worker.client_id
    assert service.client_id == db_worker.client_id
    skills.create_skill(s, worker_id, service_id)
    return Received()


def add_skills(
    skills_in: SkillsIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Received:
    picked_skills = skills_in.skills
    assert len(set((w.worker_id for w in picked_skills)))
    worker_id = picked_skills[0].worker_id

    db_worker = crud.get_worker(s, worker_id)
    if db_worker is None:
        raise WorkerNotFound

    for skill in picked_skills:
        service_id = skill.service_id
        service = services.get_service(service_id, s)

        assert service.client_id == current_user.client_id
        assert current_user.client_id == db_worker.client_id

        picked_in_db = _skill_picked(s, worker_id, service_id)
        if picked_in_db and not skill.picked:
            crud.delete_skill(s, worker_id, service_id)
        if not picked_in_db and skill.picked:
            skills.create_skill(s, worker_id, service_id)

    return Received()


def get_skills(
    client_id: int | None = Query(None),
    worker_id: int | None = Query(None),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> skills.SkillsOut:
    client_id = current_user.client_id
    return skills.get_worker_skills_including_not_picked(s, client_id, worker_id)


def my_add_skill(
    skill: SkillIn,
    s: Session = Depends(db.get_session),
) -> Received:
    worker_id = skill.worker_id
    service_id = skill.service_id

    db_worker = crud.get_worker(s, worker_id)
    db_service = crud.get_service(s, service_id)

    if db_worker is None:
        raise WorkerNotFound
    if db_service is None:
        raise app_exceptions.ServiceNotFound

    skills.create_skill(s, worker_id, service_id)
    return Received()
