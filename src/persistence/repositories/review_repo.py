from sqlalchemy.orm import Session

from src.domain.models import Review

def create_review(db: Session, review: Review):
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_review_by_user_and_event(db: Session, user_id: int, event_id: int):
    return db.query(Review).filter(
        Review.user_id == user_id, 
        Review.event_id == event_id
    ).first()
