from sqlalchemy.orm import Session

from src.application.services.friend_service import FriendService


class FriendController:
    def __init__(self, db: Session):
        self.db = db

    def accept_friend_request(self, friendship_id: int, user_id):
        friend_service = FriendService(self.db)
        return friend_service.accept_friendship(friendship_id, user_id)
    