from fastapi import Depends, Path, Query
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import users
from features.workers import schemas


def get_worker(
    worker_id: str = Path(regex=r'\d+'),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, int(worker_id))
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


def update_worker(
    worker: schemas.UpdateWorker,
    worker_id: str = Path(regex=r'\d+'),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, int(worker_id))
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, int(worker_id))
    return db_worker


def delete_worker(
    worker_id: str = Path(regex=r'\d+'),
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
