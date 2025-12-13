from sqlalchemy.orm import Session

from src.domain.models import Message

def create_message(db: Session, message: Message):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_messages_received(db: Session, user_id: int):
    return db.query(Message).filter(
        Message.destinatario_id == user_id
    ).order_by(Message.timestamp.desc()).all()

def get_messages_sent(db: Session, user_id: int):
    return db.query(Message).filter(
        Message.remetente_id == user_id
    ).order_by(Message.timestamp.desc()).all()
