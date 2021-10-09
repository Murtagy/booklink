from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String

from db import BaseModel, TableCreatedAt, TableId


class Visit(BaseModel):
    __tablename__ = "visits"

    visit_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    phone = Column(String, index=True)
    email = Column(String, index=True)
    from_datetime = Column(DateTime, index=True)
    to_datetime = Column(DateTime)
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    worker_id = Column(Integer, ForeignKey("workers.worker_id"))
    status = Column(String)
    has_notification = Column(Boolean)
    services = Column(JSON)  # [ServiceId + Q + Price, ...]


class Client(BaseModel):
    __tablename__ = "clients"

    client_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt


class Worker(BaseModel):
    __tablename__ = "workers"

    worker_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt()


class Client(BaseModel):
    __tablename__ = "customers"

    customer_id = TableId()
    display_id = Column(String, index=True)
    created_at = TableCreatedAt
