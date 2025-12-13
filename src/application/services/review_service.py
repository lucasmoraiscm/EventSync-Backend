from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain import models, schemas
from src.persistence.repositories import event_repo, registration_repo, review_repo

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def create_review(self, event_id: int, user_id: int, review_in: schemas.ReviewCreate) -> models.Review:
        event = event_repo.get_event_by_id(self.db, event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        if event.status != schemas.EventStatus.FINALIZADO:
            raise HTTPException(status_code=400, detail="Você só pode avaliar eventos finalizados")

        registration = registration_repo.get_registration(self.db, user_id, event_id)
        
        if not registration or registration.status != schemas.RegistrationStatus.APROVADA:
            raise HTTPException(status_code=403, detail="Você não participou deste evento")

        if not registration.checkins:
            raise HTTPException(status_code=400, detail="Você precisa ter feito check-in para avaliar")

        existing_review = review_repo.get_review_by_user_and_event(self.db, user_id, event_id)

        if existing_review:
            raise HTTPException(status_code=400, detail="Você já avaliou este evento")

        review = models.Review(
            event_id=event_id,
            user_id=user_id,
            nota=review_in.nota,
            comentario=review_in.comentario
        )

        # média (rating) do organizador aqui

        return review_repo.create_review(self.db, review)
