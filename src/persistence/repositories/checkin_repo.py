from sqlalchemy.orm import Session

from src.domain.models import Checkin

def create_checkin(db: Session, checkin: Checkin):
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

def get_checkins_by_event(db: Session, registration_id: int):
    return db.query(Checkin).filter(Checkin.registration_id == registration_id).all()
