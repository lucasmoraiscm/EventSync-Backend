from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain import models, schemas
from src.persistence.repositories import user_repo, friendship_repo, message_repo


class MessageService:
    def __init__(self, db: Session):
        self.db = db


    def send_message(self, sender_id: int, msg_in: schemas.MessageCreate) -> models.Message:
        destinatario = user_repo.get_user_by_id(self.db, msg_in.destinatario_id)

        if not destinatario:
            raise HTTPException(status_code=404, detail="Destinatário não encontrado")
 
        friendship = friendship_repo.get_friendship_between(self.db, sender_id, msg_in.destinatario_id)
        
        if not friendship or friendship.status != schemas.FriendshipStatus.ACEITO:
            raise HTTPException(
                status_code=403, 
                detail="Você só pode enviar mensagens para amigos confirmados."
            )

        new_msg = models.Message(
            remetente_id=sender_id,
            destinatario_id=msg_in.destinatario_id,
            titulo=msg_in.titulo,
            conteudo=msg_in.conteudo
        )
        return message_repo.create_message(self.db, new_msg)


    def list_my_messages(self, user_id: int):
        messages_received = message_repo.get_messages_received(self.db, user_id)
        messages_sent = message_repo.get_messages_sent(self.db, user_id)

        return messages_received + messages_sent
