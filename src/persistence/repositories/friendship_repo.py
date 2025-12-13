from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from src.domain.models import Friendship

def get_friendship_between(db: Session, user_a_id: int, user_b_id: int):
    return db.query(Friendship).filter(
        or_(
            and_(Friendship.solicitante_id == user_a_id, Friendship.destinatario_id == user_b_id),
            and_(Friendship.solicitante_id == user_b_id, Friendship.destinatario_id == user_a_id)
        )
    ).first()

def get_friendship_by_id(db: Session, friendship_id: int):
    return db.query(Friendship).filter(Friendship.id == friendship_id).first()

def create_friendship(db: Session, friendship: Friendship):
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship

def update_friendship(db: Session, friendship: Friendship):
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship
