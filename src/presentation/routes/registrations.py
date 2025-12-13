from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infra.storage.database import get_db
from src.domain import models, schemas
from src.presentation.dependencies import get_current_user
from src.presentation.controllers.registrations_controller import RegistrationController


router = APIRouter(prefix="/registrations", tags=["Registrations"])


@router.put("/{registration_id}/approve", response_model=schemas.RegistrationResponse)
def approve_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    registration_controller = RegistrationController(db)
    return registration_controller.approve_registration(registration_id, current_user)


@router.put("/{registration_id}/reject", response_model=schemas.RegistrationResponse)
def reject_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    registration_controller = RegistrationController(db)
    return registration_controller.reject_registration(registration_id, current_user)


@router.put("/{registration_id}/confirm-payment", response_model=schemas.RegistrationResponse)
def confirm_payment(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    registration_controller = RegistrationController(db)
    return registration_controller.confirm_payment(registration_id, current_user)


@router.get("/{registration_id}/card")
def get_virtual_card(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    registration_controller = RegistrationController(db)
    return registration_controller.get_virtual_card(registration_id, current_user)
