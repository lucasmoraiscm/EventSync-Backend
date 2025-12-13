from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infra.storage.database import get_db
from src.domain import schemas, models
from src.presentation.dependencies import get_current_user
from src.presentation.controllers.users_controller import UserController


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserResponse)
def update_user_me(
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    users_controller = UserController(db)
    return users_controller.update_user_profile(current_user, user_in)


@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user_public(user_id: int, db: Session = Depends(get_db)):
    user_controller = UserController(db)
    return user_controller.read_user_public(user_id)
