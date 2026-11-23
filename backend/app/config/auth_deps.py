from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.security import oauth2_scheme, decode_access_token
from app.entities.user import User
from app.repositories.user_repository import UserRepository
from app.enums import UserRole
from app.exceptions.custom_exceptions import UnauthorizedException, ForbiddenException


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    if not token:
        raise UnauthorizedException("Authentication token missing")
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token credentials")

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(user_id))
    if not user:
        raise UnauthorizedException("User not found")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenException("Administrator privileges required")
    return current_user
