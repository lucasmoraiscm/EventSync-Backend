from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain import models, schemas
from src.persistence.repositories import event_repo, registration_repo, checkin_repo


class CheckinService:
    def __init__(self, db: Session):
        self.db = db
    

    def perform_checkin(self, event_id: int, user_id: int, organizador: models.User):
        if organizador.role != "organizador":
            raise HTTPException(status_code=403, detail="Apenas organizadores fazem check-in")

        event = event_repo.get_event_by_id(self.db, event_id)
        
        if not event or event.organizador_id != organizador.id:
             raise HTTPException(status_code=403, detail="Você não é o organizador deste evento")

        registration = registration_repo.get_registration(self.db, user_id, event_id)
        
        if not registration or registration.status != schemas.RegistrationStatus.APROVADA:
            raise HTTPException(status_code=400, detail="Inscrição inválida ou não aprovada")
            
        checkins = checkin_repo.get_checkins_by_event(self.db, registration.id)

        if len(checkins) >= event.n_checkins_permitidos:
            raise HTTPException(status_code=400, detail="Limite de check-ins já foi atingido")
        
        new_checkin = models.Checkin(registration_id=registration.id)
        return checkin_repo.create_checkin(self.db, new_checkin)
    

    def get_virtual_card(self, registration_id: int, user: models.User):
        registration = registration_repo.get_registration_by_id(self.db, registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")
        
        is_owner = registration.user_id == user.id
        is_organizer = registration.event.organizador_id == user.id
        
        if not (is_owner or is_organizer):
            raise HTTPException(status_code=403, detail="Sem permissão para visualizar este cartão")
            
        if registration.status != schemas.RegistrationStatus.APROVADA:
            raise HTTPException(status_code=400, detail="Inscrição não aprovada. Cartão indisponível.")
        
        return {
            "registration_id": registration.id,
            "event_title": registration.event.titulo,
            "participant_name": registration.user.nome,
            "status": registration.status,
            "qr_code_data": f"EVENTSYNC:{registration.event_id}:{registration.user_id}:{registration.id}"
        }
    