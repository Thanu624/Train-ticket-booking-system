from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.entities.passenger import Passenger
from app.repositories.base_repository import BaseRepository


class PassengerRepository(BaseRepository[Passenger]):
    def __init__(self, db: Session):
        super().__init__(Passenger, db)

    def get_by_user_id(self, user_id: int) -> List[Passenger]:
        stmt = select(Passenger).where(Passenger.user_id == user_id)
        return list(self.db.scalars(stmt).all())
