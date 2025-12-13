from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain import models, schemas
from src.persistence.repositories import friendship_repo, user_repo, registration_repo


class FriendService:
    def __init__(self, db: Session):
        self.db = db


    def request_friendship(self, event_id: int, solicitante_id: int, destinatario_id: int) -> models.Friendship:
        if solicitante_id == destinatario_id:
            raise HTTPException(status_code=400, detail="Você não pode adicionar a si mesmo")

        target_user = user_repo.get_user_by_id(self.db, destinatario_id)

        if not target_user:
            raise HTTPException(status_code=404, detail="Usuário destinatário não encontrado")

        existing = friendship_repo.get_friendship_between(self.db, solicitante_id, destinatario_id)

        if existing:
            if existing.status == schemas.FriendshipStatus.ACEITO:
                 raise HTTPException(status_code=400, detail="Vocês já são amigos")
            raise HTTPException(status_code=400, detail="Já existe uma solicitação pendente entre vocês")

        reg_solicitante = registration_repo.get_registration(self.db, solicitante_id, event_id)
        reg_destinatario = registration_repo.get_registration(self.db, destinatario_id, event_id)

        if not reg_solicitante or reg_solicitante.status != schemas.RegistrationStatus.APROVADA:
            raise HTTPException(status_code=403, detail="Você precisa estar confirmado neste evento para adicionar participantes")
        
        if not reg_destinatario or reg_destinatario.status != schemas.RegistrationStatus.APROVADA:
            raise HTTPException(status_code=403, detail="O usuário destinatário não está confirmado neste evento")

        friendship = models.Friendship(
            solicitante_id=solicitante_id,
            destinatario_id=destinatario_id,
            status=schemas.FriendshipStatus.PENDENTE
        )

        return friendship_repo.create_friendship(self.db, friendship)
    

    def accept_friendship(self, friendship_id: int, user_id: int) -> models.Friendship:
        friendship = friendship_repo.get_friendship_by_id(self.db, friendship_id)
        
        if not friendship:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada")

        if friendship.destinatario_id != user_id:
            raise HTTPException(status_code=403, detail="Apenas o destinatário pode aceitar a amizade")

        if friendship.status != schemas.FriendshipStatus.PENDENTE:
            raise HTTPException(status_code=400, detail="Esta solicitação já foi respondida")

        friendship.status = schemas.FriendshipStatus.ACEITO
        return friendship_repo.update_friendship(self.db, friendship)
