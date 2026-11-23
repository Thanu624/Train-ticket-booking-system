from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import get_current_user
from app.entities.user import User
from app.services.impl.payment_service_impl import PaymentServiceImpl
from app.dtos.payment_dto import PaymentProcessDto, PaymentResponseDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/process", response_model=ApiResponse[PaymentResponseDto])
def process_simulated_payment(
    dto: PaymentProcessDto,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PaymentServiceImpl(db)
    payment = service.process_payment(current_user.id, dto)
    return ApiResponse(message="Payment processed successfully", data=payment)


@router.get("/ticket/{ticket_id}", response_model=ApiResponse[PaymentResponseDto])
def get_payment_by_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PaymentServiceImpl(db)
    payment = service.get_payment_by_ticket(ticket_id)
    return ApiResponse(message="Payment details retrieved", data=payment)
