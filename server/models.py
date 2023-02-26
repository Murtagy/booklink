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

    slots: list["Slot"] = Relationship(back_populates="worker_owner")

    def assure_id(self, client_id: int) -> None:
        if self.client_id != client_id:
            raise NoPermission


class VisitWorker(SQLModel, table=True):
    __tablename__ = "visit_workers"

    id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    name: str
    job_title: str
    client_id: int = Field(foreign_key="clients.client_id")
    # ^ Worker +
    slot_id: int = Field(foreign_key="slots.slot_id", unique=True)
    slot: "Slot" = Relationship(back_populates="worker")


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
    minutes: int
    description: str | None
    client_id: int = Field(foreign_key="clients.client_id")

    def assure_id(self, client_id: int) -> None:
        if self.client_id != client_id:
            raise NoPermission


class VisitService(SQLModel, table=True):
    __tablename__ = "visit_services"

    id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    name: str
    price: float | None
    price_to: float | None
    minutes: int
    description: str | None
    client_id: int = Field(foreign_key="clients.client_id")

    # ^ Service +
    slot_id: int = Field(foreign_key="slots.slot_id")
    slot: "Slot" = Relationship(back_populates="services")

    def assure_id(self, client_id: int) -> None:
        if self.client_id != client_id:
            raise NoPermission


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

    client_id: int = Field(foreign_key="clients.client_id")
    customer_id: int | None = Field(foreign_key="customers.customer_id")

    phone: str | None
    email: str | None
    has_notification: bool | None

    worker_id: int = Field(foreign_key="workers.worker_id")  # owner (e.g. for "my visits today")
    worker_owner: Worker = Relationship(back_populates="slots")

    services: list[VisitService] = Relationship(back_populates="slot")
    worker: "VisitWorker" = Relationship(back_populates="slot")
