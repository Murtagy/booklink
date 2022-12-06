from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)

from db import BaseModel, ModelImpl, TableCreatedAt, TableId


class Visit(BaseModel, ModelImpl):
    __tablename__ = "visits"

    visit_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    worker_id = Column(Integer, ForeignKey("workers.worker_id"))
    phone = Column(String, index=True)
    email = Column(String, index=True)
    status = Column(String)
    customer_description = Column(String)
    has_notification = Column(Boolean)
    services = Column(JSON)  # [ServiceId + Q + Price, ...]
    slot_id = Column(Integer, ForeignKey("slots.slot_id"))


class Client(BaseModel, ModelImpl):
    __tablename__ = "clients"

    client_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt

    blocked_datetime = Column(DateTime(timezone=True))
    name = Column(String, index=True)


class Worker(BaseModel, ModelImpl):
    __tablename__ = "workers"

    worker_id = TableId()
    created_at = TableCreatedAt()
    display_id = Column(String, index=True)

    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    display_name = Column(String)
    display_job_title = Column(String)
    display_description = Column(String)
    photo_id = Column(Integer, ForeignKey("files.file_id"))
    use_company_schedule = Column(Boolean, nullable=False)
    # use_company_services = Column(Boolean, nullable=False)


class File(BaseModel, ModelImpl):
    __tablename__ = "files"

    file_id = TableId()
    created_at = TableCreatedAt()
    display_id = Column(String, index=True)
    file = Column(LargeBinary, nullable=False)
    content_type = Column(String, nullable=False)
    # owner
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    worker_id = Column(Integer, ForeignKey("workers.worker_id"))


class Customer(BaseModel, ModelImpl):
    __tablename__ = "customers"

    customer_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()


# how Workers get their services
class Service(BaseModel, ModelImpl):
    __tablename__ = "services"

    service_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()
    # created_by

    name = Column(String, nullable=False)
    price = Column(Float)
    price_lower_bound = Column(Float)
    price_higher_bound = Column(Float)
    seconds = Column(Integer, nullable=False)  # length
    display_description = Column(String)
    description = Column(String)
    blocked_datetime = Column(DateTime(timezone=True))
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    # worker_inheritance = Column(String)  # give all


# TODO: rename to Skills
class WorkerService(BaseModel, ModelImpl):
    # abilities of worker
    # idea is that an owner will manually check what services each worker should have
    __tablename__ = "workers_services"

    rel_id = TableId()
    created_at = TableCreatedAt()

    worker_id = Column(Integer, ForeignKey("workers.worker_id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)
    # rel_type = Column(String)  # include


class User(BaseModel, ModelImpl):
    __tablename__ = "users"

    user_id = TableId()
    display_id = Column(String, index=True)
    client_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = TableCreatedAt()

    email = Column(String, index=True, unique=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    blocked_datetime = Column(DateTime(timezone=True))
    # is_active = Column(Boolean,default=True)


class Token(BaseModel, ModelImpl):
    __tablename__ = "tokens"

    token_id = TableId()
    access_token = Column(String, unique=True, index=True, nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class WeeklySlot(BaseModel, ModelImpl):
    __tablename__ = "weekly_slots"

    active_from = Column(DateTime(timezone=True))
    slot_id = TableId()
    created_at = TableCreatedAt()

    worker_id = Column(
        Integer, ForeignKey("workers.worker_id")
    )  # when worker_id is null then it is client owned
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    schedule_by_day = Column(JSON, nullable=False)


class Slot(BaseModel, ModelImpl):
    __tablename__ = "slots"

    slot_id = TableId()
    created_at = TableCreatedAt()
    name = Column(String)
    slot_type = Column(String, nullable=False)  # busy/visit/available
    active = Column(Boolean, default=True, nullable=False)

    from_datetime = Column(DateTime(timezone=True), nullable=False)
    to_datetime = Column(DateTime(timezone=True), nullable=False)

    worker_id = Column(Integer, ForeignKey("workers.worker_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
