from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infra.storage.database import get_db
from src.domain import schemas
from src.presentation.controllers.auth_controller import AuthController


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    auth_controller = AuthController(db)
    return auth_controller.register(user)


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    auth_controller = AuthController(db)
    return auth_controller.login(form_data.username, form_data.password)
