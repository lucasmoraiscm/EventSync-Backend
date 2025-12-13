from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from src.domain import models, schemas
from src.persistence.repositories import event_repo


class EventService:
    def __init__(self, db: Session):
        self.db = db


    def create_event(self, event_in: schemas.EventCreate, user: models.User) -> models.Event:
        if user.role != "organizador":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Apenas organizadores podem criar eventos"
            )
        
        event = models.Event(
            **event_in.model_dump(),
            organizador_id=user.id,
            status="rascunho" 
        )
        
        return event_repo.create_event(self.db, event)
    

    def update_event(self, event_id: int, event_in: schemas.EventUpdate, user: models.User):
        event = self.get_event_details(event_id)
        
        if event.organizador_id != user.id:
            raise HTTPException(status_code=403, detail="Apenas o organizador pode editar este evento")
        
        update_data = event_in.model_dump(exclude_unset=True)

        return event_repo.update_event(self.db, event, update_data)


    def list_events(self, skip: int = 0, limit: int = 100) -> List[models.Event]:
        return event_repo.get_events(self.db, skip=skip, limit=limit)
    

    def get_event_details(self, event_id: int) -> models.Event:
        event = event_repo.get_event_by_id(self.db, event_id)
        
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        return event

    
    def change_event_status(self, event_id: int, status: str, user: models.User):
        return self.update_event(event_id, schemas.EventUpdate(status=status), user)
