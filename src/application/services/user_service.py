from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.domain import models, schemas
from src.persistence.repositories import user_repo


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def get_user_public_profile(self, user_id: int) -> models.User:
        user = user_repo.get_user_by_id(self.db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuário não encontrado"
            )
        
        return user
    
    
    def update_user_profile(self, current_user: models.User, user_in: schemas.UserUpdate) -> models.User:
        update_data = user_in.model_dump(exclude_unset=True)
        
        if not update_data:
            return current_user
            
        return user_repo.update_user(self.db, current_user, update_data)
