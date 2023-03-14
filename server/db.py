from typing import AsyncGenerator

from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import create_engine

LITE_DB = "sqlite:////Users/murtagy/Dev/booklink/sql_app.db"
DB_URL = LITE_DB

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_session() -> AsyncGenerator[Session, None]:
    # note: https://github.com/tiangolo/fastapi/issues/1241
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
