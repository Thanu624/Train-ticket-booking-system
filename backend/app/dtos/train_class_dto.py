from typing import Optional
from pydantic import BaseModel, Field
from app.enums import ClassType


class TrainClassCreateDto(BaseModel):
    train_id: int
    class_type: ClassType
    fare: float = Field(..., gt=0)
    total_seats: int = Field(..., gt=0)
    available_seats: Optional[int] = None


class TrainClassUpdateDto(BaseModel):
    fare: Optional[float] = Field(None, gt=0)
    total_seats: Optional[int] = Field(None, gt=0)
    available_seats: Optional[int] = Field(None, ge=0)
