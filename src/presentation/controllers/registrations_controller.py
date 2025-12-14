from sqlalchemy.orm import Session

from src.domain import models
from src.application.services.registration_service import RegistrationService
from src.application.services.checkin_service import CheckinService


class RegistrationController:
    def __init__(self, db: Session):
        self.db = db

    
    def approve_registration(self, registration_id: int, user: models.User):
        registration_service = RegistrationService(self.db)
        return registration_service.approve_registration(registration_id, user)
    

    def reject_registration(self, registration_id: int, user: models.User):
        registration_service = RegistrationService(self.db)
        return registration_service.reject_registration(registration_id, user)
    

    def confirm_payment(self, registration_id: int, user: models.User):
        registration_service = RegistrationService(self.db)
        return registration_service.confirm_payment(registration_id, user)


    def get_virtual_card(self, registration_id: int, user: models.User):
        checkin_service = CheckinService(self.db)
        return checkin_service.get_virtual_card(registration_id, user)
    

    def list_my_registrations(self, user_id: int):
        registration_service = RegistrationService(self.db)
        return registration_service.list_registrations_user(user_id)
    