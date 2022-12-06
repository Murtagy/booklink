import datetime
from typing import Generator, Optional, Type, TypeVar

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import func

LITE_DB = "sqlite:///./sql_app.db"
# PROD_DB = "postgresql://user:password@postgresserver/db"
DB_URL = LITE_DB

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()


T = TypeVar("T", bound="BaseModel")


class ModelImpl:
    @classmethod
    def get_by_id(cls: Type[T], db: Session, id: int) -> Optional[T]:  # type: ignore[misc]
        model = cls
        return db.get(model, id)


def TableId() -> Column[int]:
    return Column(Integer, primary_key=True, index=True, unique=True)


def TableCreatedAt() -> Column[datetime.datetime]:
    return Column(DateTime(timezone=True), default=func.now())


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
