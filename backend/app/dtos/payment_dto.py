from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.enums import PaymentStatus


class PaymentProcessDto(BaseModel):
    payment_id: int
    payment_method: str = Field(default="CARD", pattern=r"^(CARD|UPI|NETBANKING)$")
    simulated_outcome: Optional[PaymentStatus] = PaymentStatus.SUCCESS


class PaymentResponseDto(BaseModel):
    id: int
    ticket_id: int
    amount: float
    payment_status: PaymentStatus
    transaction_id: str
    created_at: datetime

    class Config:
        from_attributes = True
