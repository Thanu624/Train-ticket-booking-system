from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.entities.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email.strip().lower())
        return self.db.scalars(stmt).first()
