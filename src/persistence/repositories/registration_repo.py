from sqlalchemy.orm import Session

from src.domain.models import Registration

def create_registration(db: Session, registration: Registration):
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def get_registration(db: Session, user_id: int, event_id: int):
    return db.query(Registration).filter(
        Registration.user_id == user_id, 
        Registration.event_id == event_id
    ).first()

def get_registrations_by_event(db: Session, event_id: int):
    return db.query(Registration).filter(Registration.event_id == event_id).all()

def get_registration_by_id(db: Session, registration_id: int) -> Registration:
    return db.query(Registration).filter(Registration.id == registration_id).first()

def update_registration_status(db: Session, registration: Registration, new_status: str):
    registration.status = new_status
    db.add(registration)
    db.commit()
    db.refresh(registration)
    return registration

def get_registrations_by_user_id(db: Session, user_id: int) -> Registration:
    return db.query(Registration).filter(Registration.user_id == user_id).all()
