from fastapi import Depends, Path, Query
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

from .. import app_exceptions, crud, db, models
from . import services, skills, users
from ..app_exceptions import WorkerNotFound 


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
    services: list[SkillIn]


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
        # filter for skilled workers only
        service_ids = {int(s) for s in services.split(",")}
        db_workers_tmp = db_workers.copy()
        db_workers = []
        for worker in db_workers_tmp:
            worker_services = crud.get_services(s, client_id, worker_id=worker.worker_id)
            worker_services_ids = {s.service_id for s in worker_services}
            if not service_ids.issubset(worker_services_ids):
                continue
            db_workers.append(worker)

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
    assert len(set((w.worker_id for w in skills_in.services)))
    worker_id = skills_in.services[0].worker_id

    db_worker = crud.get_worker(s, worker_id)
    if db_worker is None:
        raise WorkerNotFound

    for updated_service in skills_in.services:
        service_id = updated_service.service_id
        service = services.get_service(service_id, s)

        assert service.client_id == current_user.client_id
        assert current_user.client_id == db_worker.client_id

        picked_in_db = _skill_picked(s, worker_id, service_id)
        if picked_in_db and not updated_service.picked:
            crud.delete_skill(s, worker_id, service_id)
        if not picked_in_db and updated_service.picked:
            skills.create_skill(s, worker_id, service_id)

    return Received()


def get_skills(
    client_id: int,
    worker_id: int | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> skills.SkillsOut:
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
