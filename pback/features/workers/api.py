from fastapi import Depends, Path, Query
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions
import crud
import db
import models
from features import services, skills, users
from features.workers import schemas


def get_worker(
    worker_id: str = Path(regex=r"\d+"),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, int(worker_id))
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


def update_worker(
    worker: schemas.UpdateWorker,
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
) -> None:
    return None


def get_workers_by_client(
    client_id: int,
    services: str | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> schemas.OutWorkers:
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

    return schemas.OutWorkers(workers=db_workers)


def get_workers(
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> schemas.OutWorkers:
    db_workers = crud.get_workers(s, current_user.client_id)

    return schemas.OutWorkers(workers=db_workers)


def create_worker(
    worker: schemas.CreateWorker,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    # TODO notify user that he needs to add company schedule
    # if worker.use_company_schedule:
    # wl = crud.get_client_weeklyslot(s, current_user.client_id)
    # if wl is None:
    # raise HTTPException(428, "Schedule needs to be created first")
    client_id = current_user.client_id
    db_worker = crud.create_worker(s, worker, client_id)
    return db_worker


def _skill_picked(s: Session, worker_id: int, service_id: int) -> bool:
    ws = crud.get_skill(s, worker_id, service_id)
    if ws is None:
        return False
    else:
        return True


# endpoints:
def add_skill(
    skill: schemas.SkillIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> schemas.Received:
    worker_id = skill.worker_id
    service_id = skill.service_id

    db_worker = crud.get_worker(s, worker_id)
    service = services.get_service(service_id, s)

    if db_worker is None:
        raise app_exceptions.WorkerNotFound
    if service is None:
        raise app_exceptions.ServiceNotFound

    assert current_user.client_id == db_worker.client_id
    assert service.client_id == db_worker.client_id
    skills.create_skill(s, worker_id, service_id)
    return schemas.Received()


def add_skills(
    skills_in: schemas.SkillsIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> schemas.Received:
    assert len(set((w.worker_id for w in skills_in.services)))
    worker_id = skills_in.services[0].worker_id

    db_worker = crud.get_worker(s, worker_id)
    if db_worker is None:
        raise app_exceptions.WorkerNotFound

    for updated_service in skills_in.services:
        service_id = updated_service.service_id
        service = services.get_service_must(service_id, s)

        assert service.client_id == current_user.client_id
        assert current_user.client_id == db_worker.client_id

        picked_in_db = _skill_picked(s, worker_id, service_id)
        if picked_in_db and not updated_service.picked:
            crud.delete_skill(s, worker_id, service_id)
        if not picked_in_db and updated_service.picked:
            skills.create_skill(s, worker_id, service_id)

    return schemas.Received()


def get_skills(
    client_id: int,
    worker_id: int | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> skills.SkillsOut:
    return skills.get_worker_skills_including_not_picked(s, client_id, worker_id)


def my_add_skill(
    skill: schemas.SkillIn,
    s: Session = Depends(db.get_session),
) -> schemas.Received:
    worker_id = skill.worker_id
    service_id = skill.service_id

    db_worker = crud.get_worker(s, worker_id)
    db_service = crud.get_service(s, service_id)

    if db_worker is None:
        raise app_exceptions.WorkerNotFound
    if db_service is None:
        raise app_exceptions.ServiceNotFound

    skills.create_skill(s, worker_id, service_id)
    return schemas.Received()
