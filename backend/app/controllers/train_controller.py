from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import require_admin
from app.entities.user import User
from app.services.impl.train_service_impl import TrainServiceImpl
from app.dtos.train_dto import TrainCreateDto, TrainUpdateDto, TrainResponseDto, TrainSearchDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/trains", tags=["Trains"])


@router.get("", response_model=ApiResponse[List[TrainResponseDto]])
def get_or_search_trains(
    source: Optional[str] = Query(None, description="Source station name"),
    destination: Optional[str] = Query(None, description="Destination station name"),
    journey_date: Optional[date] = Query(None, description="Journey date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = TrainServiceImpl(db)
    if source and destination:
        j_date = journey_date or date.today()
        search_dto = TrainSearchDto(source=source, destination=destination, journey_date=j_date)
        trains = service.search_train(search_dto)
        return ApiResponse(message=f"Found {len(trains)} trains", data=trains)

    trains = service.get_all_trains(skip=skip, limit=limit)
    return ApiResponse(message="Trains fetched successfully", data=trains)


@router.get("/{train_id}", response_model=ApiResponse[TrainResponseDto])
def get_train_by_id(train_id: int, db: Session = Depends(get_db)):
    service = TrainServiceImpl(db)
    train = service.get_train_by_id(train_id)
    return ApiResponse(message="Train details fetched", data=train)


@router.post("", response_model=ApiResponse[TrainResponseDto], status_code=status.HTTP_201_CREATED)
def add_train(
    dto: TrainCreateDto,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainServiceImpl(db)
    train = service.add_train(dto)
    return ApiResponse(message="Train created successfully", data=train)


@router.put("/{train_id}", response_model=ApiResponse[TrainResponseDto])
def update_train(
    train_id: int,
    dto: TrainUpdateDto,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainServiceImpl(db)
    train = service.update_train(train_id, dto)
    return ApiResponse(message="Train updated successfully", data=train)


@router.delete("/{train_id}", response_model=ApiResponse[bool])
def delete_train(
    train_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainServiceImpl(db)
    success = service.delete_train(train_id)
    return ApiResponse(message="Train deleted successfully", data=success)
