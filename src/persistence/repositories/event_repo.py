from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from sqlalchemy import or_

from src.domain.models import Event

def create_event(db: Session, event: Event):
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_events(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    titulo: Optional[str] = None,
    tipo: Optional[str] = None,
    data_inicio: Optional[datetime] = None,
    organizador_id: Optional[int] = None
):
    query = db.query(Event)

    if organizador_id:
        query = query.filter(Event.organizador_id == organizador_id)

    else:
        query = query.filter(Event.status != "rascunho")

        if titulo:
            query = query.filter(Event.titulo.ilike(f"%{titulo}%"))
        
        if tipo:
            query = query.filter(Event.tipo == tipo)
            
        if data_inicio:
            query = query.filter(Event.data_inicio >= data_inicio)

    return query.offset(skip).limit(limit).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def update_event(db: Session, db_event: Event, event_update: dict):
    for key, value in event_update.items():
        setattr(db_event, key, value)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
