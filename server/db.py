from typing import AsyncGenerator

from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import create_engine
import os

LITE_DB = f"sqlite:///{os.environ['DB_FILE']}"
DB_URL = LITE_DB

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, future=True)


async def get_session() -> AsyncGenerator[Session, None]:
    # note: https://github.com/tiangolo/fastapi/issues/1241
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield session
    finally:
        session.close()
