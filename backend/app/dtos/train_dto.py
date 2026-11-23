from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator


class TrainSearchDto(BaseModel):
    source: str = Field(..., min_length=2, max_length=80)
    destination: str = Field(..., min_length=2, max_length=80)
    journey_date: date

    @model_validator(mode="after")
    def validate_stations_and_date(self):
        if self.source.strip().lower() == self.destination.strip().lower():
            raise ValueError("Source and destination stations cannot be the same")
        if self.journey_date < date.today():
            raise ValueError("Journey date cannot be in the past")
        return self


class TrainCreateDto(BaseModel):
    train_number: str = Field(..., min_length=3, max_length=20)
    train_name: str = Field(..., min_length=3, max_length=100)
    source: str = Field(..., min_length=2, max_length=80)
    destination: str = Field(..., min_length=2, max_length=80)
    departure_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    arrival_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")


class TrainUpdateDto(BaseModel):
    train_name: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None


class TrainClassResponseDto(BaseModel):
    id: int
    train_id: int
    class_type: str
    fare: float
    total_seats: int
    available_seats: int

    class Config:
        from_attributes = True


class TrainResponseDto(BaseModel):
    id: int
    train_number: str
    train_name: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    train_classes: List[TrainClassResponseDto] = []

    class Config:
        from_attributes = True
