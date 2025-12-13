from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.infra.storage.database import get_db
from src.domain import schemas, models
from src.presentation.dependencies import get_current_user
from src.presentation.controllers.messages_controller import MessageController


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/", response_model=schemas.MessageResponse)
def send_message(
    msg_in: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message_controller = MessageController(db)
    return message_controller.send_message(current_user.id, msg_in)


@router.get("/", response_model=List[schemas.MessageResponse])
def list_my_messages(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message_controller = MessageController(db)
    return message_controller.list_my_messages(current_user.id)
