from fastapi import Depends, Path
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
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


def update_worker(
    worker: schemas.UpdateWorker,
    worker_id: str = Path(regex=r'\d+'),
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, worker_id)
    return db_worker


def delete_worker(
    worker_id: str = Path(regex=r'\d+'),
) -> None:
    return None


def get_workers_by_client(
    client_id: int,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> schemas.OutWorkers:
    db_workers = crud.get_workers(s, client_id)

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
