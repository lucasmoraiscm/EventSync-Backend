from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infra.storage.database import get_db
from src.domain import schemas, models
from src.presentation.dependencies import get_current_user
from src.presentation.controllers.events_controller import EventController


router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event_in: schemas.EventCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.create_event(event_in, current_user)    


@router.put("/{event_id}", response_model=schemas.EventResponse)
def edit_event(
    event_id: int,
    event_in: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.edit_event(event_id, event_in, current_user)


@router.get("/", response_model=List[schemas.EventResponse])
def list_events(
    skip: int = 0, 
    limit: int = 100,
    titulo: Optional[str] = Query(None, description="Filtrar por título"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (gratuito/pago)"),
    data_inicio: Optional[datetime] = Query(None, description="Filtrar eventos após esta data"),
    organizador_id: Optional[int] = Query(None, description="Filtrar eventos de um organizador específico"),
    db: Session = Depends(get_db)
):
    event_controller = EventController(db)
    return event_controller.list_events(
        skip, 
        limit, 
        titulo, 
        tipo, 
        data_inicio, 
        organizador_id
    )


@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event_details(
    event_id: int, 
    db: Session = Depends(get_db)
):
    event_controller = EventController(db)
    return event_controller.get_event_details(event_id)


@router.post("/{event_id}/open-inscriptions", response_model=schemas.EventResponse)
def open_inscriptions(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.open_inscriptions(event_id, current_user)


@router.post("/{event_id}/close-inscriptions", response_model=schemas.EventResponse)
def close_inscriptions(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.close_inscriptions(event_id, current_user)


@router.post("/{event_id}/publish", response_model=schemas.EventResponse)
def publish_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.publish_event(event_id, current_user)


@router.post("/{event_id}/register", response_model=schemas.RegistrationResponse)
def register_in_event(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.register_in_event(event_id, current_user.id)


@router.get("/{event_id}/registrations", response_model=List[schemas.RegistrationResponse])
def list_event_registrations(
    event_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.list_event_registrations(event_id, current_user)


@router.post("/{event_id}/checkin")
def checkin(
    event_id: int, 
    checkin_data: schemas.CheckinRequest, # No futuro, QR Code
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.checkin(event_id, checkin_data.user_id, current_user)


@router.post("/{event_id}/friend-request", response_model=schemas.FriendshipResponse)
def send_friend_request(
    event_id: int,
    friend_data: schemas.FriendshipCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.send_friend_request(event_id, current_user.id, friend_data.destinatario_id)


@router.post("/{event_id}/reviews", response_model=schemas.ReviewResponse)
def review_event(
    event_id: int,
    review_in: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.review_event(event_id, current_user.id, review_in)


@router.get("/{event_id}/certificate")
def download_certificate(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.download_certificate(event_id, current_user.id)


@router.get("/{event_id}/export")
def export_event_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    event_controller = EventController(db)
    return event_controller.export_event_registrations(event_id, current_user)
