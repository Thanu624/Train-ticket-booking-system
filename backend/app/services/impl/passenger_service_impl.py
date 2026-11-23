from typing import List
from sqlalchemy.orm import Session
from app.entities.passenger import Passenger
from app.repositories.passenger_repository import PassengerRepository
from app.services.interfaces.passenger_service import IPassengerService
from app.dtos.passenger_dto import PassengerCreateDto, PassengerUpdateDto, PassengerResponseDto
from app.exceptions.custom_exceptions import NotFoundException, ForbiddenException


class PassengerServiceImpl(IPassengerService):
    def __init__(self, db: Session):
        self.db = db
        self.passenger_repo = PassengerRepository(db)

    def add_passenger(self, user_id: int, dto: PassengerCreateDto) -> PassengerResponseDto:
        passenger = Passenger(
            user_id=user_id,
            name=dto.name.strip(),
            age=dto.age,
            gender=dto.gender.upper(),
            mobile_number=dto.mobile_number.strip(),
        )
        self.passenger_repo.create(passenger)
        self.db.commit()
        self.db.refresh(passenger)
        return PassengerResponseDto.model_validate(passenger)

    def update_passenger(self, passenger_id: int, user_id: int, dto: PassengerUpdateDto) -> PassengerResponseDto:
        passenger = self.passenger_repo.get_by_id(passenger_id)
        if not passenger:
            raise NotFoundException("Passenger not found")
        if passenger.user_id != user_id:
            raise ForbiddenException("You cannot modify this passenger record")

        if dto.name is not None:
            passenger.name = dto.name.strip()
        if dto.age is not None:
            passenger.age = dto.age
        if dto.gender is not None:
            passenger.gender = dto.gender.upper()
        if dto.mobile_number is not None:
            passenger.mobile_number = dto.mobile_number.strip()

        self.passenger_repo.update(passenger)
        self.db.commit()
        self.db.refresh(passenger)
        return PassengerResponseDto.model_validate(passenger)

    def get_passenger_by_id(self, passenger_id: int) -> PassengerResponseDto:
        passenger = self.passenger_repo.get_by_id(passenger_id)
        if not passenger:
            raise NotFoundException("Passenger not found")
        return PassengerResponseDto.model_validate(passenger)

    def get_all_passengers(self, user_id: int) -> List[PassengerResponseDto]:
        passengers = self.passenger_repo.get_by_user_id(user_id)
        return [PassengerResponseDto.model_validate(p) for p in passengers]
