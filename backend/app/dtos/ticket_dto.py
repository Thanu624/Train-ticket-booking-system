from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.enums import TicketStatus
from app.dtos.train_dto import TrainResponseDto, TrainClassResponseDto
from app.dtos.passenger_dto import PassengerResponseDto


class TicketRequestDto(BaseModel):
    train_id: int
    train_class_id: int
    passenger_id: Optional[int] = None
    # Support inline passenger creation for smooth checkout
    passenger_name: Optional[str] = None
    passenger_age: Optional[int] = None
    passenger_gender: Optional[str] = None
    passenger_mobile: Optional[str] = None
    journey_date: date


class TicketPaymentSummaryDto(BaseModel):
    id: int
    amount: float
    payment_status: str
    transaction_id: str

    class Config:
        from_attributes = True


class TicketResponseDto(BaseModel):
    id: int
    pnr_number: str
    user_id: int
    train_id: int
    train_class_id: int
    passenger_id: int
    journey_date: date
    seat_number: Optional[str] = None
    coach_number: Optional[str] = None
    ticket_status: TicketStatus
    created_at: datetime
    train: Optional[TrainResponseDto] = None
    train_class: Optional[TrainClassResponseDto] = None
    passenger: Optional[PassengerResponseDto] = None
    payment: Optional[TicketPaymentSummaryDto] = None

    class Config:
        from_attributes = True


class TicketCancelResponseDto(BaseModel):
    ticket_id: int
    pnr_number: str
    previous_status: TicketStatus
    new_status: TicketStatus = TicketStatus.CANCELLED
    seat_released: Optional[str] = None
    refund_status: str = "REFUND_INITIATED"
    refund_amount: float
