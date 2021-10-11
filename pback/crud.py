import datetime
import uuid
from datetime import timedelta
from typing import Optional, Union

from sqlalchemy.orm import Session

import schemas
from models import Token, User, Visit
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
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    # ? refresh
    return db_user


def get_user_by_user_id(db: Session, user_id: Union[int, str]) -> Optional[User]:
    user_id = int(user_id)
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_token_id(db: Session, token_id: str) -> Optional[User]:
    t = db.query(Token).filter(Token.token_id == int(token_id)).first()
    if t is None or t.expires < datetime.datetime.now():
        return None

    assert t is not None
    user_id = t.user_id
    assert user_id is not None
    return get_user_by_user_id(db, user_id)


def create_user_token(db: Session, user_id: int) -> Token:
    token = Token(
        access_token=str(uuid.uuid4()),
        expires=datetime.datetime.now() + timedelta(weeks=4),
        user_id=user_id,
    )
    db.add(token)
    db.commit()
    return token
