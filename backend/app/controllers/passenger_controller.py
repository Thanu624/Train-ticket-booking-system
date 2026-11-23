from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import get_current_user
from app.entities.user import User
from app.services.impl.passenger_service_impl import PassengerServiceImpl
from app.dtos.passenger_dto import PassengerCreateDto, PassengerUpdateDto, PassengerResponseDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.get("", response_model=ApiResponse[List[PassengerResponseDto]])
def get_user_passengers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PassengerServiceImpl(db)
    passengers = service.get_all_passengers(current_user.id)
    return ApiResponse(message="Passengers retrieved", data=passengers)


@router.post("", response_model=ApiResponse[PassengerResponseDto], status_code=status.HTTP_201_CREATED)
def add_passenger(
    dto: PassengerCreateDto,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PassengerServiceImpl(db)
    passenger = service.add_passenger(current_user.id, dto)
    return ApiResponse(message="Passenger created successfully", data=passenger)


@router.put("/{passenger_id}", response_model=ApiResponse[PassengerResponseDto])
def update_passenger(
    passenger_id: int,
    dto: PassengerUpdateDto,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PassengerServiceImpl(db)
    passenger = service.update_passenger(passenger_id, current_user.id, dto)
    return ApiResponse(message="Passenger updated successfully", data=passenger)
