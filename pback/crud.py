from typing import Optional

from sqlalchemy.orm import Session

import schemas
from models import User, Visit
from utils.users import hash_password, make_salt


def get_visit(db: Session, visit_id: int) -> Optional[Visit]:
    return db.query(Visit).filter(Visit.visit_id == visit_id).first()


def create_visit(db: Session, visit: schemas.InVisit) -> Visit:
    db_visit = Visit(client_id=visit.client_id, phone=visit.phone, email=visit.email)
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)  # why refresh?
    return db_visit


def create_user(db: Session, user: schemas.UserCreate) -> User:
    salt = make_salt()
    hashed_password = hash_password(user.password, salt)
    db_user = User(**user.dict(), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    # ? refresh
    return db_user
