from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import require_admin
from app.entities.user import User
from app.services.impl.train_class_service_impl import TrainClassServiceImpl
from app.dtos.train_class_dto import TrainClassCreateDto, TrainClassUpdateDto
from app.dtos.train_dto import TrainClassResponseDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/train-classes", tags=["Train Classes"])


@router.post("", response_model=ApiResponse[TrainClassResponseDto], status_code=status.HTTP_201_CREATED)
def add_train_class(
    dto: TrainClassCreateDto,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainClassServiceImpl(db)
    train_class = service.add_class(dto)
    return ApiResponse(message="Train class added successfully", data=train_class)


@router.put("/{class_id}", response_model=ApiResponse[TrainClassResponseDto])
def update_train_class(
    class_id: int,
    dto: TrainClassUpdateDto,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainClassServiceImpl(db)
    train_class = service.update_class(class_id, dto)
    return ApiResponse(message="Train class updated successfully", data=train_class)


@router.get("/train/{train_id}", response_model=ApiResponse[List[TrainClassResponseDto]])
def get_classes_for_train(train_id: int, db: Session = Depends(get_db)):
    service = TrainClassServiceImpl(db)
    classes = service.get_all_classes(train_id)
    return ApiResponse(message="Classes fetched successfully", data=classes)


@router.delete("/{class_id}", response_model=ApiResponse)
def delete_train_class(
    class_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    service = TrainClassServiceImpl(db)
    service.delete_class(class_id)
    return ApiResponse(message="Train class deleted successfully", data=None)
