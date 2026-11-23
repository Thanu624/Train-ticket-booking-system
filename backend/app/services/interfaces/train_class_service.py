from abc import ABC, abstractmethod
from typing import List
from app.dtos.train_class_dto import TrainClassCreateDto, TrainClassUpdateDto
from app.dtos.train_dto import TrainClassResponseDto


class ITrainClassService(ABC):
    @abstractmethod
    def add_class(self, dto: TrainClassCreateDto) -> TrainClassResponseDto:
        pass

    @abstractmethod
    def update_class(self, class_id: int, dto: TrainClassUpdateDto) -> TrainClassResponseDto:
        pass

    @abstractmethod
    def get_class_by_id(self, class_id: int) -> TrainClassResponseDto:
        pass

    @abstractmethod
    def get_all_classes(self, train_id: int) -> List[TrainClassResponseDto]:
        pass

    @abstractmethod
    def delete_class(self, class_id: int) -> None:
        pass
