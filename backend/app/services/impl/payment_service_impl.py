from sqlalchemy.orm import Session
from app.entities.payment import Payment
from app.entities.ticket import Ticket
from app.enums import PaymentStatus, TicketStatus
from app.repositories.payment_repository import PaymentRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.train_class_repository import TrainClassRepository
from app.services.interfaces.payment_service import IPaymentService
from app.dtos.payment_dto import PaymentProcessDto, PaymentResponseDto
from app.exceptions.custom_exceptions import NotFoundException, BadRequestException


class PaymentServiceImpl(IPaymentService):
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.ticket_repo = TicketRepository(db)
        self.class_repo = TrainClassRepository(db)

    def process_payment(self, user_id: int, dto: PaymentProcessDto) -> PaymentResponseDto:
        payment = self.payment_repo.get_by_id(dto.payment_id)
        if not payment:
            raise NotFoundException("Payment record not found")

        ticket = self.ticket_repo.get_by_id(payment.ticket_id)
        if not ticket:
            raise NotFoundException("Associated ticket not found")

        if payment.payment_status == PaymentStatus.SUCCESS:
            raise BadRequestException("Payment has already been successfully processed")

        outcome = dto.simulated_outcome or PaymentStatus.SUCCESS

        if outcome == PaymentStatus.SUCCESS:
            payment.payment_status = PaymentStatus.SUCCESS
            # Confirmed ticket
        else:
            payment.payment_status = PaymentStatus.FAILED
            # Failed payment releases seat
            if ticket.ticket_status == TicketStatus.BOOKED:
                train_class = self.class_repo.get_with_lock(ticket.train_class_id)
                if train_class:
                    train_class.available_seats = min(
                        train_class.total_seats, train_class.available_seats + 1
                    )
                    self.class_repo.update(train_class)
            ticket.ticket_status = TicketStatus.CANCELLED
            self.ticket_repo.update(ticket)

        self.payment_repo.update(payment)
        self.db.commit()
        self.db.refresh(payment)
        return PaymentResponseDto.model_validate(payment)

    def get_payment_by_ticket(self, ticket_id: int) -> PaymentResponseDto:
        payment = self.payment_repo.get_by_ticket_id(ticket_id)
        if not payment:
            raise NotFoundException("Payment record not found")
        return PaymentResponseDto.model_validate(payment)
