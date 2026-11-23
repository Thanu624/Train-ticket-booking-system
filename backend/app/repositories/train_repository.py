from typing import List, Optional
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.entities.train import Train
from app.repositories.base_repository import BaseRepository


class TrainRepository(BaseRepository[Train]):
    def __init__(self, db: Session):
        super().__init__(Train, db)

    def get_by_train_number(self, train_number: str) -> Optional[Train]:
        stmt = select(Train).where(Train.train_number == train_number.strip().upper())
        return self.db.scalars(stmt).first()

    def get_with_classes(self, train_id: int) -> Optional[Train]:
        stmt = (
            select(Train)
            .where(Train.id == train_id)
            .options(selectinload(Train.train_classes))
        )
        return self.db.scalars(stmt).first()

    def search(self, source: str, destination: str) -> List[Train]:
        stmt = (
            select(Train)
            .where(
                Train.source.ilike(f"%{source.strip()}%"),
                Train.destination.ilike(f"%{destination.strip()}%"),
            )
            .options(selectinload(Train.train_classes))
        )
        return list(self.db.scalars(stmt).all())
