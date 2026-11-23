from abc import ABC, abstractmethod
from typing import List
from app.dtos.passenger_dto import PassengerCreateDto, PassengerUpdateDto, PassengerResponseDto


class IPassengerService(ABC):
    @abstractmethod
    def add_passenger(self, user_id: int, dto: PassengerCreateDto) -> PassengerResponseDto:
        pass

    @abstractmethod
    def update_passenger(self, passenger_id: int, user_id: int, dto: PassengerUpdateDto) -> PassengerResponseDto:
        pass

    @abstractmethod
    def get_passenger_by_id(self, passenger_id: int) -> PassengerResponseDto:
        pass

    @abstractmethod
    def get_all_passengers(self, user_id: int) -> List[PassengerResponseDto]:
        pass
