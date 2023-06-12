from typing import Optional

from fastapi import Depends, Query
from pydantic import BaseModel as BM, validator
from sqlalchemy.orm import Session  # type: ignore

from .. import crud, db, models
from ..app_exceptions import ServiceNotFound
from . import users


class CreateService(BM):
    name: str
    price: Optional[float]
    price_to: Optional[float]
    minutes: int
    description: Optional[str]

    @validator("price", "price_to", pre=True)
    def empty_str_to_none(cls, value) -> str:
        # for easier client update/create code
        if value == '':
            return None
        return value


class UpdateService(CreateService):
    pass


class CreateServiceWithClientId(CreateService):
    client_id: int


class OutService(BM):
    service_id: int
    client_id: int
    name: str
    price: Optional[float]
    price_to: Optional[float]
    minutes: int
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


def get_service_optional(
    service_id: int,
    s: Session = Depends(db.get_session),
) -> Optional[OutService]:
    db_service = crud.get_service(s, service_id)
    if db_service:
        return OutService.from_orm(db_service)
    return None


def get_service(
    service_id: int,
    s: Session = Depends(db.get_session),
) -> OutService:
    db_service = crud.get_service(s, service_id)
    if db_service is None:
        raise ServiceNotFound
    return OutService.from_orm(db_service)


def get_services(
    client_id: int,
    worker_id: Optional[int] = None,
    s: Session = Depends(db.get_session),
) -> OutServices:
    db_services = crud.get_services(s, client_id, worker_id=worker_id)
    services = [OutService.from_orm(s) for s in db_services]
    return OutServices(services=services)


def get_services_by_ids(
    services_ids: list[int],
    s: Session = Depends(db.get_session),
) -> list[OutService]:
    db_services = crud.get_services_by_ids(s, services_ids)
    return [OutService.from_orm(s) for s in db_services]


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


def get_services_by_user(
    current_user: models.User = Depends(users.get_current_user),
    worker_id: Optional[int] = Query(None),
    s: Session = Depends(db.get_session),
) -> OutServices:
    client_id = current_user.client_id
    services = get_services(client_id, worker_id=worker_id, s=s)
    return services


def update_service(
    service_id: int,
    r: UpdateService,
    current_user: models.User = Depends(users.get_current_user),
    s: Session = Depends(db.get_session),
) -> OutService:
    service = crud.get_service(s, service_id, not_found=ServiceNotFound)
    service.assure_id(current_user.client_id)
    db_service = crud.update_service(s, service_id, r)
    return OutService.from_orm(db_service)


def delete_service(
    service_id: int,
    current_user: models.User = Depends(users.get_current_user),
    s: Session = Depends(db.get_session),
) -> None:
    service = crud.get_service(s, service_id, not_found=ServiceNotFound)
    service.assure_id(current_user.client_id)
    crud.delete_service(s, service_id)
