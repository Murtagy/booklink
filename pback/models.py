import datetime
from typing import Any

from sqlalchemy import Column, LargeBinary
from sqlalchemy.sql import func
from sqlmodel import JSON, Field, SQLModel


class Visit(SQLModel, table=True):
    __tablename__ = "visits"

    visit_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    customer_id: int | None = Field(foreign_key="customers.customer_id")
    client_id: int = Field(foreign_key="clients.client_id")
    worker_id: int | None = Field(foreign_key="workers.worker_id")
    phone: str | None
    email: str | None
    status: str
    customer_description: str | None
    has_notification: bool
    services: list[Any] = Field(sa_column=Column(JSON))  # [ServiceId + Q + Price, ...]
    schedule_by_day: list[dict[str, Any]] = Field(sa_column=Column(JSON), nullable=False)
    slot_id: int = Field(foreign_key="slots.slot_id")


class Client(SQLModel, table=True):
    __tablename__ = "clients"

    client_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    blocked_datetime: datetime.datetime | None
    name: str


class Worker(SQLModel, table=True):
    __tablename__ = "workers"

    worker_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    client_id: int = Field(foreign_key="clients.client_id")
    name: str
    job_title: str
    use_company_schedule: bool
    # use_company_services = Column(Boolean, nullable=False)


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
    price_lower_bound: float | None
    price_higher_bound: float | None
    seconds: int
    description: str | None
    blocked_datetime: datetime.datetime | None
    client_id: int = Field(foreign_key="clients.client_id")
    # worker_inheritance = Column(String)  # give all


class Skill(SQLModel, table=True):
    # abilities of worker
    # idea is that an owner will manually check what services each worker should have
    __tablename__ = "skills"

    rel_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())

    worker_id: int = Field(foreign_key="workers.worker_id")
    service_id: int = Field(foreign_key="services.service_id")


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True, index=True, unique=True)
    client_id: int = Field(foreign_key="clients.client_id")
    created_at: datetime.datetime = Field(default=func.now())

    email: str
    username: str
    hashed_password: str


class Token(SQLModel, table=True):
    __tablename__ = "tokens"

    token_id: int = Field(primary_key=True, index=True, unique=True)
    access_token: str = Field(unique=True, index=True, nullable=False)
    expires: datetime.datetime
    user_id: int = Field(foreign_key="users.user_id", nullable=False)


class WeeklySlot(SQLModel, table=True):
    __tablename__ = "weekly_slots"

    active_from: datetime.datetime | None = None
    slot_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())
    worker_id: int | None = Field(foreign_key="workers.worker_id")
    client_id: int = Field(foreign_key="clients.client_id")
    schedule_by_day: dict[str, Any] = Field(sa_column=Column(JSON), nullable=False)


class Slot(SQLModel, table=True):
    __tablename__ = "slots"

    slot_id: int = Field(primary_key=True, index=True, unique=True)
    created_at: datetime.datetime = Field(default=func.now())
    name: str
    slot_type: str  # busy/visit/available
    active: bool = True

    from_datetime: datetime.datetime
    to_datetime: datetime.datetime

    worker_id: int = Field(foreign_key="workers.worker_id")
    client_id: int = Field(foreign_key="clients.client_id")
