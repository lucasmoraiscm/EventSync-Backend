from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain import models, schemas
from src.persistence.repositories import event_repo, registration_repo


class RegistrationService:
    def __init__(self, db: Session):
        self.db = db
    

    def register_user(self, event_id: int, user_id: int) -> models.Registration:
        event = event_repo.get_event_by_id(self.db, event_id)

        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")

        existing = registration_repo.get_registration(self.db, user_id, event_id)

        if existing:
            raise HTTPException(status_code=400, detail="Usuário já inscrito neste evento")
        
        if event.max_inscricoes:
            registrations = registration_repo.get_registrations_by_event(self.db, event_id)
            
            if len(registrations) >= event.max_inscricoes:
                raise HTTPException(status_code=400, detail="Evento já atingiu o limite de participantes")
        
        status_inicial = schemas.RegistrationStatus.APROVADA
        
        if event.tipo == "pago":
             status_inicial = "aguardando_pagamento"
        elif event.exige_aprovacao:
            status_inicial = schemas.RegistrationStatus.PENDENTE

        registration = models.Registration(
            user_id=user_id,
            event_id=event_id,
            status=status_inicial
        )

        return registration_repo.create_registration(self.db, registration)


    def list_event_registrations(self, event_id: int, user: models.User):
        event = event_repo.get_event_by_id(self.db, event_id)
        
        if event.organizador_id != user.id:
            raise HTTPException(status_code=403, detail="Sem permissão para ver inscritos")
            
        return registration_repo.get_registrations_by_event(self.db, event_id)
    

    def approve_registration(self, registration_id: int, user: models.User) -> models.Registration:
        registration = registration_repo.get_registration_by_id(self.db, registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")

        if registration.event.organizador_id != user.id:
            raise HTTPException(
                status_code=403, 
                detail="Apenas o organizador do evento pode gerenciar esta inscrição"
            )
        
        return registration_repo.update_registration_status(self.db, registration, schemas.RegistrationStatus.APROVADA)


    def reject_registration(self, registration_id: int, user: models.User) -> models.Registration:
        registration = registration_repo.get_registration_by_id(self.db, registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")

        if registration.event.organizador_id != user.id:
            raise HTTPException(
                status_code=403, 
                detail="Apenas o organizador do evento pode gerenciar esta inscrição"
            )
        
        return registration_repo.update_registration_status(self.db, registration, schemas.RegistrationStatus.RECUSADA)


    def confirm_payment(self, registration_id: int, user: models.User) -> models.Registration:
        registration = registration_repo.get_registration_by_id(self.db, registration_id)

        if not registration:
            raise HTTPException(status_code=404, detail="Inscrição não encontrada")

        if registration.event.organizador_id != user.id:
            raise HTTPException(
                status_code=403, 
                detail="Apenas o organizador do evento pode gerenciar esta inscrição"
            )
        
        return registration_repo.update_registration_status(self.db, registration, schemas.RegistrationStatus.APROVADA)
