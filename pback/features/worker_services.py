from fastapi import Depends
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions
import crud
import db
import models
from features import users


class WorkerServiceIn(BM):
    worker_id: int
    service_id: int


class Received(BM):
    msg: str = "Received"


async def add_worker_service(
    worker_service: WorkerServiceIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Received:
    worker_id = worker_service.worker_id
    service_id = worker_service.service_id

    db_worker = crud.get_worker(s, worker_id)
    db_service = crud.get_service(s, service_id)

    if db_worker is None:
        raise app_exceptions.WorkerNotFound
    if db_service is None:
        raise app_exceptions.ServiceNotFound

    assert current_user.client_id == db_worker.client_id
    assert db_service.client_id == db_worker.client_id
    crud.create_worker_service(s, worker_id, service_id)
    return Received()


async def my_add_worker_service(
    worker_service: WorkerServiceIn,
    s: Session = Depends(db.get_session),
) -> Received:
    worker_id = worker_service.worker_id
    service_id = worker_service.service_id

    db_worker = crud.get_worker(s, worker_id)
    db_service = crud.get_service(s, service_id)

    if db_worker is None:
        raise app_exceptions.WorkerNotFound
    if db_service is None:
        raise app_exceptions.ServiceNotFound

    crud.create_worker_service(s, worker_id, service_id)
    return Received()
