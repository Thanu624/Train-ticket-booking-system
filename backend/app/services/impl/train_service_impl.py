from typing import List
from sqlalchemy.orm import Session
from app.entities.train import Train
from app.repositories.train_repository import TrainRepository
from app.services.interfaces.train_service import ITrainService
from app.dtos.train_dto import TrainCreateDto, TrainUpdateDto, TrainResponseDto, TrainSearchDto
from app.exceptions.custom_exceptions import ConflictException, NotFoundException


class TrainServiceImpl(ITrainService):
    def __init__(self, db: Session):
        self.db = db
        self.train_repo = TrainRepository(db)

    def add_train(self, dto: TrainCreateDto) -> TrainResponseDto:
        existing = self.train_repo.get_by_train_number(dto.train_number)
        if existing:
            raise ConflictException(f"Train number '{dto.train_number}' already exists")

        train = Train(
            train_number=dto.train_number.strip().upper(),
            train_name=dto.train_name.strip(),
            source=dto.source.strip().title(),
            destination=dto.destination.strip().title(),
            departure_time=dto.departure_time,
            arrival_time=dto.arrival_time,
        )
        self.train_repo.create(train)
        self.db.commit()
        self.db.refresh(train)
        return TrainResponseDto.model_validate(train)

    def update_train(self, train_id: int, dto: TrainUpdateDto) -> TrainResponseDto:
        train = self.train_repo.get_with_classes(train_id)
        if not train:
            raise NotFoundException(f"Train with ID {train_id} not found")

        if dto.train_name is not None:
            train.train_name = dto.train_name.strip()
        if dto.source is not None:
            train.source = dto.source.strip().title()
        if dto.destination is not None:
            train.destination = dto.destination.strip().title()
        if dto.departure_time is not None:
            train.departure_time = dto.departure_time
        if dto.arrival_time is not None:
            train.arrival_time = dto.arrival_time

        self.train_repo.update(train)
        self.db.commit()
        self.db.refresh(train)
        return TrainResponseDto.model_validate(train)

    def delete_train(self, train_id: int) -> bool:
        train = self.train_repo.get_by_id(train_id)
        if not train:
            raise NotFoundException(f"Train with ID {train_id} not found")
        self.train_repo.delete(train)
        self.db.commit()
        return True

    def get_train_by_id(self, train_id: int) -> TrainResponseDto:
        train = self.train_repo.get_with_classes(train_id)
        if not train:
            raise NotFoundException(f"Train with ID {train_id} not found")
        return TrainResponseDto.model_validate(train)

    def get_all_trains(self, skip: int = 0, limit: int = 100) -> List[TrainResponseDto]:
        trains = self.train_repo.get_all(skip=skip, limit=limit)
        return [TrainResponseDto.model_validate(t) for t in trains]

    def search_train(self, dto: TrainSearchDto) -> List[TrainResponseDto]:
        trains = self.train_repo.search(dto.source, dto.destination)
        return [TrainResponseDto.model_validate(t) for t in trains]
