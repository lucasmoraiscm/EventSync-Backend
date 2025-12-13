from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional

from src.domain import models, schemas
from src.persistence.repositories import user_repo
from src.core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db


    def register_user(self, user_in: schemas.UserCreate) -> models.User:
        existing_user = user_repo.get_user_by_email(self.db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado no sistema."
            )
        
        hashed_password = get_password_hash(user_in.senha)

        new_user = models.User(
            nome=user_in.nome,
            email=user_in.email,
            senha_hash=hashed_password,
            cidade=user_in.cidade,
            foto_url=user_in.foto_url,
            role=user_in.role
        )

        return user_repo.create_user(self.db, new_user)


    def authenticate_user(self, email: str, password: str) -> Optional[models.User]:
        user = user_repo.get_user_by_email(self.db, email)

        if not user:
            return None
        
        if not verify_password(password, user.senha_hash):
            return None
        
        return user


    def create_token_for_user(self, user: models.User):
        access_token = create_access_token(data={"sub": user.email}, )
        return {"access_token": access_token, "token_type": "bearer"}
