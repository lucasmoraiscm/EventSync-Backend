from sqlalchemy.orm import Session

from src.domain import models, schemas
from src.application.services.user_service import UserService


class UserController:
    def __init__(self, db: Session):
        self.db = db


    def update_user_profile(self, current_user: models.User, user_in: schemas.UserUpdate):
        user_service = UserService(self.db)
        return user_service.update_user_profile(current_user, user_in)


    def read_user_public(self, user_id: int):
        user_service = UserService(self.db)
        return user_service.get_user_public_profile(user_id)
