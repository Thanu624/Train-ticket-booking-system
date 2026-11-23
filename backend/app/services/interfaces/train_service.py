from abc import ABC, abstractmethod
from typing import List
from app.dtos.train_dto import TrainCreateDto, TrainUpdateDto, TrainResponseDto, TrainSearchDto


class ITrainService(ABC):
    @abstractmethod
    def add_train(self, dto: TrainCreateDto) -> TrainResponseDto:
        pass

    @abstractmethod
    def update_train(self, train_id: int, dto: TrainUpdateDto) -> TrainResponseDto:
        pass

    @abstractmethod
    def delete_train(self, train_id: int) -> bool:
        pass

    @abstractmethod
    def get_train_by_id(self, train_id: int) -> TrainResponseDto:
        pass

    @abstractmethod
    def get_all_trains(self, skip: int = 0, limit: int = 100) -> List[TrainResponseDto]:
        pass

    @abstractmethod
    def search_train(self, dto: TrainSearchDto) -> List[TrainResponseDto]:
        pass
