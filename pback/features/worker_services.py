from fastapi import Depends, Query
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import app_exceptions
import crud
import db
import models
from features import services, users


class WorkerServiceIn(BM):
    worker_id: int
    service_id: int
    picked: bool = True


class WorkerServicesIn(BM):
    services: list[WorkerServiceIn]


class Received(BM):
    msg: str = "Received"


def add_worker_service_endpoint(
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


def add_worker_services_endpoint(
    worker_services: WorkerServicesIn,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> Received:
    assert len(set((w.worker_id for w in worker_services.services)))
    worker_id = worker_services.services[0].worker_id

    db_worker = crud.get_worker(s, worker_id)
    if db_worker is None:
        raise app_exceptions.WorkerNotFound

    for updated_service in worker_services.services:
        service_id = updated_service.service_id
        service = crud.get_service(s, service_id)

        assert service is not None
        assert service.client_id == current_user.client_id
        assert current_user.client_id == db_worker.client_id

        picked_in_db = worker_service_picked(s, worker_id, service_id)
        if picked_in_db and not updated_service.picked:
            crud.delete_worker_service(s, worker_id, service_id)
        if not picked_in_db and updated_service.picked:
            crud.create_worker_service(s, worker_id, service_id)

    return Received()


def worker_service_picked(s: Session, worker_id: int, service_id: int) -> bool:
    ws = crud.get_worker_service(s, worker_id, service_id)
    if ws is None:
        return False
    else:
        return True


def my_add_worker_service(
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


class OutWorkerService(services.OutService):
    picked: bool


class OutServices(BM):
    services: list[OutWorkerService]


def get_services_by_worker_endpoint(
    client_id: int,
    worker_id: int | None = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> OutServices:
    out_services: list[OutWorkerService] = []

    client_services = crud.get_services(s, client_id)
    worker_services = crud.get_services(s, client_id, worker_id=worker_id)

    for cs in client_services:
        worker_picked_service = cs in worker_services
        pre_service = services.OutService.from_orm(cs)
        service_out = OutWorkerService(
            picked=worker_picked_service, **pre_service.dict()
        )
        out_services.append(service_out)

    return OutServices(services=out_services)
