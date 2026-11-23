from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.entities.train_class import TrainClass
from app.enums import ClassType
from app.repositories.base_repository import BaseRepository


class TrainClassRepository(BaseRepository[TrainClass]):
    def __init__(self, db: Session):
        super().__init__(TrainClass, db)

    def get_by_train_and_type(self, train_id: int, class_type: ClassType) -> Optional[TrainClass]:
        stmt = select(TrainClass).where(
            TrainClass.train_id == train_id,
            TrainClass.class_type == class_type,
        )
        return self.db.scalars(stmt).first()

    def get_by_train_id(self, train_id: int) -> List[TrainClass]:
        stmt = select(TrainClass).where(TrainClass.train_id == train_id)
        return list(self.db.scalars(stmt).all())

    def get_with_lock(self, train_class_id: int) -> Optional[TrainClass]:
        """Locks the train class row for concurrency prevention."""
        stmt = (
            select(TrainClass)
            .where(TrainClass.id == train_class_id)
            .with_for_update()
        )
        return self.db.scalars(stmt).first()
