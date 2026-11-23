from typing import List
from sqlalchemy.orm import Session
from app.entities.train_class import TrainClass
from app.repositories.train_class_repository import TrainClassRepository
from app.repositories.train_repository import TrainRepository
from app.services.interfaces.train_class_service import ITrainClassService
from app.dtos.train_class_dto import TrainClassCreateDto, TrainClassUpdateDto
from app.dtos.train_dto import TrainClassResponseDto
from app.exceptions.custom_exceptions import NotFoundException, ConflictException


class TrainClassServiceImpl(ITrainClassService):
    def __init__(self, db: Session):
        self.db = db
        self.class_repo = TrainClassRepository(db)
        self.train_repo = TrainRepository(db)

    def add_class(self, dto: TrainClassCreateDto) -> TrainClassResponseDto:
        train = self.train_repo.get_by_id(dto.train_id)
        if not train:
            raise NotFoundException(f"Train with ID {dto.train_id} not found")

        existing = self.class_repo.get_by_train_and_type(dto.train_id, dto.class_type)
        if existing:
            raise ConflictException(f"Class '{dto.class_type.value}' already exists on Train {dto.train_id}")

        avail = dto.available_seats if dto.available_seats is not None else dto.total_seats
        train_class = TrainClass(
            train_id=dto.train_id,
            class_type=dto.class_type,
            fare=dto.fare,
            total_seats=dto.total_seats,
            available_seats=avail,
        )
        self.class_repo.create(train_class)
        self.db.commit()
        self.db.refresh(train_class)
        return TrainClassResponseDto.model_validate(train_class)

    def update_class(self, class_id: int, dto: TrainClassUpdateDto) -> TrainClassResponseDto:
        train_class = self.class_repo.get_by_id(class_id)
        if not train_class:
            raise NotFoundException(f"Train class with ID {class_id} not found")

        if dto.fare is not None:
            train_class.fare = dto.fare
        if dto.total_seats is not None:
            train_class.total_seats = dto.total_seats
        if dto.available_seats is not None:
            train_class.available_seats = dto.available_seats

        self.class_repo.update(train_class)
        self.db.commit()
        self.db.refresh(train_class)
        return TrainClassResponseDto.model_validate(train_class)

    def get_class_by_id(self, class_id: int) -> TrainClassResponseDto:
        train_class = self.class_repo.get_by_id(class_id)
        if not train_class:
            raise NotFoundException(f"Train class with ID {class_id} not found")
        return TrainClassResponseDto.model_validate(train_class)

    def get_all_classes(self, train_id: int) -> List[TrainClassResponseDto]:
        classes = self.class_repo.get_by_train_id(train_id)
        return [TrainClassResponseDto.model_validate(c) for c in classes]

    def delete_class(self, class_id: int) -> None:
        train_class = self.class_repo.get_by_id(class_id)
        if not train_class:
            raise NotFoundException(f"Train class with ID {class_id} not found")
        self.class_repo.delete(train_class)
        self.db.commit()
