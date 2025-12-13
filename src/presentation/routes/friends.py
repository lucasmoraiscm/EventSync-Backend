from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infra.storage.database import get_db
from src.domain import schemas, models
from src.presentation.dependencies import get_current_user
from src.presentation.controllers.friends_controller import FriendController


router = APIRouter(prefix="/friends", tags=["Friends"])


@router.put("/{friendship_id}/accept", response_model=schemas.FriendshipResponse)
def accept_friend_request(
    friendship_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    friend_controller = FriendController(db)
    return friend_controller.accept_friend_request(friendship_id, current_user.id)
