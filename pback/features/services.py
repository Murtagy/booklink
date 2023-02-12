from typing import Optional

from fastapi import Depends, Query
from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

import crud
import db
import models
from features import users


class CreateService(BM):
    name: str
    price: Optional[float]
    price_lower_bound: Optional[float]
    price_higher_bound: Optional[float]
    seconds: int
    description: Optional[str]


class CreateServiceWithClientId(CreateService):
    client_id: int


class OutService(BM):
    service_id: int
    client_id: int
    name: str
    price: Optional[float]
    price_lower_bound: Optional[float]
    price_higher_bound: Optional[float]
    seconds: int
    description: str | None
    currency: str = "рублей"

    class Config:
        orm_mode = True


class OutServices(BM):
    services: list[OutService]


def create_service(
    service: CreateService,
    s: Session = Depends(db.get_session),
    current_user: models.User = Depends(users.get_current_user),
) -> models.Service:
    client_id = current_user.client_id
    db_service = crud.create_service(s, service, client_id)
    return db_service


def my_create_service(
    service: CreateServiceWithClientId,
    s: Session = Depends(db.get_session),
) -> models.Service:
    client_id = service.client_id
    db_service = crud.create_service(s, CreateService(**service.dict()), client_id)
    return db_service


def get_service(
    service_id: int,
    s: Session = Depends(db.get_session),
) -> Optional[OutService]:
    db_service = crud.get_service(s, service_id)
    if db_service:
        return OutService.from_orm(db_service)
    return None


def get_service_must(
    service_id: int,
    s: Session = Depends(db.get_session),
) -> OutService:
    db_service = crud.get_service(s, service_id)
    if db_service is None:
        raise AssertionError(f"Must have service {service_id}")
    return OutService.from_orm(db_service)


def get_services(
    client_id: int,
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
) -> OutServices:
    db_services = crud.get_services(s, client_id, worker_id=worker_id)
    services = [OutService.from_orm(s) for s in db_services]
    return OutServices(services=services)


def get_service_by_client(
    client_id: int,
    service_id: int,
    s: Session = Depends(db.get_session),
) -> Optional[models.Service]:
    return crud.get_service(s, service_id)


def get_services_by_client(
    client_id: int,
    worker_id: Optional[int] = Query(None),
    s: Session = Depends(db.get_session),
    # current_user: models.User = Depends(users.get_current_user),
) -> OutServices:
    services = get_services(client_id, worker_id=worker_id, s=s)
    return services
