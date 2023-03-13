# from typing import Generator
# from sqlalchemy.orm import declarative_base  # 2.0 style
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import create_engine

LITE_DB = "sqlite:////Users/murtagy/Dev/booklink/sql_app.db"
DB_URL = LITE_DB

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    return SessionLocal()
    # using the generator
    # try:
    # yield session
    # finally:
    # session.close()
