from typing import Optional

from fastapi import Depends
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import users


class CreateWorker(BM):
    name: str
    job_title: str
    use_company_schedule: Optional[bool]


class UpdateWorker(BM):
    # worker_id: int
    name: Optional[str]
    job_title: Optional[str]
    use_company_schedule: Optional[bool]

    display_name: Optional[str]
    display_job_title: Optional[str]
    display_description: Optional[str]
    photo_id: Optional[int]


class OutWorker(BM):
    worker_id: str
    name: str
    job_title: str
    display_name: Optional[str]
    display_job_title: Optional[str]
    display_description: Optional[str]
    use_company_schedule: bool
    photo_id: Optional[int]

    class Config:
        orm_mode = True


class OutWorkers(BM):
    workers: list[OutWorker]


def get_worker_endpoint(
    worker_id: int,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None

    assert current_user.client_id == db_worker.client_id

    return db_worker


def update_worker_endpoint(
    worker_id: int,
    worker: UpdateWorker,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Worker:
    db_worker = crud.get_worker(s, worker_id)
    assert db_worker is not None
    assert current_user.client_id == db_worker.client_id

    db_worker = crud.update_worker(s, worker, worker_id)
    return db_worker


def delete_worker_endpoint(worker_id: str) -> None:
    return None


def get_workers_by_client_endpoint(
    client_id: int,
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, client_id)

    return OutWorkers(workers=db_workers)


def get_workers_endpoint(
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> OutWorkers:
    db_workers = crud.get_workers(s, current_user.client_id)

    return OutWorkers(workers=db_workers)


def create_worker_endpoint(
    worker: CreateWorker,
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
