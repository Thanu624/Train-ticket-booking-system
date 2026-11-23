from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.auth_deps import get_current_user
from app.entities.user import User
from app.services.impl.ticket_service_impl import TicketServiceImpl
from app.dtos.ticket_dto import TicketRequestDto, TicketResponseDto, TicketCancelResponseDto
from app.dtos.common_dto import ApiResponse

router = APIRouter(prefix="/tickets", tags=["Tickets & Booking"])


@router.post("/book", response_model=ApiResponse[TicketResponseDto], status_code=status.HTTP_201_CREATED)
def book_ticket(
    dto: TicketRequestDto,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TicketServiceImpl(db)
    ticket = service.book_ticket(current_user.id, dto)
    return ApiResponse(message="Ticket booked successfully", data=ticket)


@router.get("/my-bookings", response_model=ApiResponse[List[TicketResponseDto]])
def get_my_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TicketServiceImpl(db)
    tickets = service.get_all_tickets(current_user.id, skip=skip, limit=limit)
    return ApiResponse(message="User tickets retrieved", data=tickets)


@router.get("/pnr/{pnr}", response_model=ApiResponse[TicketResponseDto])
def get_ticket_by_pnr(pnr: str, db: Session = Depends(get_db)):
    service = TicketServiceImpl(db)
    ticket = service.get_ticket_by_pnr(pnr)
    return ApiResponse(message="Ticket retrieved by PNR", data=ticket)


@router.post("/{ticket_id}/cancel", response_model=ApiResponse[TicketCancelResponseDto])
def cancel_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = TicketServiceImpl(db)
    result = service.cancel_ticket(ticket_id, current_user.id)
    return ApiResponse(message="Ticket cancelled successfully", data=result)
