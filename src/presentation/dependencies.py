from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.infra.storage.database import get_db
from src.persistence.repositories.user_repo import get_user_by_email


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    request: Request, 
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = getattr(request.state, "user_email", None)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária"
        )
    
    user = get_user_by_email(db, email=email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )
    
    return user
