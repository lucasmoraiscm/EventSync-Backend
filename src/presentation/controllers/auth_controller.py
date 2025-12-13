from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.domain import schemas
from src.application.services.auth_service import AuthService


class AuthController:
    def __init__(self, db: Session):
        self.db = db


    def register(self, user: schemas.UserCreate):
        auth_service = AuthService(self.db)
        return auth_service.register_user(user)
    

    def login(self, username: str, password: str):
        auth_service = AuthService(self.db)
    
        user = auth_service.authenticate_user(username, password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Credenciais incorretas (email ou senha inválidos)"
            )
        
        return auth_service.create_token_for_user(user)
