from sqlalchemy.orm import Session

from models import Visit


def get_visit(db: Session, visit_id: int) -> Visit:
    return db.query(Visit).filter(Visit.visit_id == visit_id).first()
