from sqlalchemy.orm import Session

from src.domain import schemas
from src.application.services.message_service import MessageService


class MessageController:
    def __init__(self, db: Session):
        self.db = db

    
    def send_message(self, user_id: int, msg: schemas.MessageCreate):
        message_service = MessageService(self.db)
        return message_service.send_message(user_id, msg)
    
    def list_my_messages(self, user_id: int):
        message_service = MessageService(self.db)
        return message_service.list_my_messages(user_id)
    
