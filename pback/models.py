import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from db import BaseModel, TableCreatedAt, TableId


class Visit(BaseModel):
    __tablename__ = "visits"

    visit_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    worker_id = Column(Integer, ForeignKey("workers.worker_id"))
    phone = Column(String, index=True)
    email = Column(String, index=True)
    from_datetime = Column(DateTime(timezone=True), index=True)
    to_datetime = Column(DateTime(timezone=True))
    status = Column(String)
    has_notification = Column(Boolean)
    services = Column(JSON)  # [ServiceId + Q + Price, ...]


class Client(BaseModel):
    __tablename__ = "clients"

    client_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt

    blocked = Column(Boolean, nullable=False, default=False)
    blocked_datetime = Column(DateTime(timezone=True))


class Worker(BaseModel):
    __tablename__ = "workers"

    worker_id = TableId()
    created_at = TableCreatedAt()
    display_id = Column(String, index=True)

    name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    display_name = Column(String)
    display_job_title = Column(String)
    display_description = Column(String)
    use_company_schedule = Column(Boolean, nullable=False)
    photo_id = Column(Integer, ForeignKey("files.file_id"))


class File(BaseModel):
    __tablename__ = "files"

    file_id = TableId()
    created_at = TableCreatedAt()
    display_id = Column(String, index=True)
    file = Column(LargeBinary, nullable=False)
    content_type = Column(String, nullable=False)
    # owner
    client_id = Column(Integer, ForeignKey("clients.client_id"))


class Customer(BaseModel):
    __tablename__ = "customers"

    customer_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()


class User(BaseModel):
    __tablename__ = "users"

    user_id = TableId()
    display_id = Column(String, index=True)
    client_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = TableCreatedAt()

    email = Column(String, index=True, unique=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    blocked = Column(Boolean, nullable=False, default=False)
    blocked_datetime = Column(DateTime(timezone=True))
    # is_active = Column(Boolean, default=True)



class Token(BaseModel):
    __tablename__ = "tokens"

    token_id = TableId()
    access_token = Column(String, unique=True, index=True, nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
