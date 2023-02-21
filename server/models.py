import datetime
import enum

from sqlalchemy import Column, LargeBinary
from sqlalchemy.sql import func
from sqlmodel import Field, Relationship, SQLModel

from .app_exceptions import NoPermission


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    name: str


class Worker(SQLModel, table=True):
    __tablename__ = "workers"

    worker_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    client_id: int = Field(foreign_key="clients.client_id")
    name: str
    job_title: str


class File(SQLModel, table=True):
    __tablename__ = "files"

    file_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    file: bytes = Field(sa_column=Column(LargeBinary, nullable=False))
    content_type: str
    # owner
    client_id: int = Field(foreign_key="clients.client_id")
    worker_id: int | None = Field(foreign_key="workers.worker_id")


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())


class Service(SQLModel, table=True):
    __tablename__ = "services"

    service_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    name: str
    price: float | None
    price_to: float | None
    seconds: int
    description: str | None
    blocked_datetime: datetime.datetime | None
    client_id: int = Field(foreign_key="clients.client_id")


class Skill(SQLModel, table=True):
    # abilities of worker
    # idea is that an owner will manually check what services each worker should have
    __tablename__ = "skills"

    created_at: datetime.datetime = Field(default=func.now())

    worker_id: int = Field(foreign_key="workers.worker_id", primary_key=True)
    service_id: int = Field(
        foreign_key="services.service_id",
        primary_key=True,
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True, index=True, unique=True)
    client_id: int = Field(foreign_key="clients.client_id")
    created_at: datetime.datetime = Field(default=func.now())

    email: str
    username: str
    hashed_password: str

    def assure_id(self, client_id: int) -> None:
        if self.client_id != client_id:
            raise NoPermission


class Token(SQLModel, table=True):
    __tablename__ = "tokens"

    token_id: int = Field(primary_key=True, index=True, unique=True)
    access_token: str = Field(unique=True, index=True, nullable=False)
    expires: datetime.datetime
    user_id: int = Field(foreign_key="users.user_id", nullable=False)


class VisitServices(SQLModel, table=True):
    # adds services to a visit' slot
    __tablename__ = "visit_services"

    # rel_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    slot_id: int = Field(foreign_key="slots.slot_id", primary_key=True)
    service_id: int = Field(foreign_key="services.service_id", primary_key=True)


class SlotType(enum.StrEnum):
    AVAILABLE = "available"
    BUSY = "busy"
    VISIT = "visit"


class Slot(SQLModel, table=True):
    __tablename__ = "slots"

    slot_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())
    slot_type: SlotType
    status: str | None

    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    worker_id: int = Field(foreign_key="workers.worker_id")
    client_id: int = Field(foreign_key="clients.client_id")
    customer_id: int | None = Field(foreign_key="customers.customer_id")

    phone: str | None
    email: str | None
    has_notification: bool | None
    services: list[Service] = Relationship(link_model=VisitServices)
