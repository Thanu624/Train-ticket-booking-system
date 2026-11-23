import uuid
from typing import List
from sqlalchemy.orm import Session
from app.entities.ticket import Ticket
from app.entities.payment import Payment
from app.entities.passenger import Passenger
from app.enums import TicketStatus, PaymentStatus
from app.repositories.ticket_repository import TicketRepository
from app.repositories.train_class_repository import TrainClassRepository
from app.repositories.passenger_repository import PassengerRepository
from app.services.interfaces.ticket_service import ITicketService
from app.dtos.ticket_dto import TicketRequestDto, TicketResponseDto, TicketCancelResponseDto
from app.utils.pnr_generator import generate_pnr
from app.utils.seat_allocator import allocate_coach_and_seat
from app.exceptions.custom_exceptions import NotFoundException, BadRequestException, ForbiddenException


class TicketServiceImpl(ITicketService):
    def __init__(self, db: Session):
        self.db = db
        self.ticket_repo = TicketRepository(db)
        self.class_repo = TrainClassRepository(db)
        self.passenger_repo = PassengerRepository(db)

    def book_ticket(self, user_id: int, dto: TicketRequestDto) -> TicketResponseDto:
        # 1. Pessimistic row locking on target TrainClass to prevent race conditions & double-booking
        train_class = self.class_repo.get_with_lock(dto.train_class_id)
        if not train_class:
            raise NotFoundException(f"Train class with ID {dto.train_class_id} not found")

        # 2. Resolve or create passenger
        passenger_id = dto.passenger_id
        if not passenger_id:
            if not dto.passenger_name or not dto.passenger_age:
                raise BadRequestException("Either passenger_id or complete passenger details must be provided")
            passenger = Passenger(
                user_id=user_id,
                name=dto.passenger_name.strip(),
                age=dto.passenger_age,
                gender=(dto.passenger_gender or "MALE").upper(),
                mobile_number=(dto.passenger_mobile or "9999999999").strip(),
            )
            self.passenger_repo.create(passenger)
            passenger_id = passenger.id
        else:
            passenger = self.passenger_repo.get_by_id(passenger_id)
            if not passenger:
                raise NotFoundException("Passenger not found")

        # 3. Determine current bookings on journey date
        confirmed_count = self.ticket_repo.count_by_status(
            train_class.id, dto.journey_date, TicketStatus.BOOKED
        )
        waiting_count = self.ticket_repo.count_by_status(
            train_class.id, dto.journey_date, TicketStatus.WAITING
        )

        status, coach, seat = allocate_coach_and_seat(
            class_type=train_class.class_type,
            confirmed_count=confirmed_count,
            total_capacity=train_class.total_seats,
            waiting_count=waiting_count,
        )

        # Update available seats
        if status == TicketStatus.BOOKED:
            train_class.available_seats = max(0, train_class.total_seats - (confirmed_count + 1))
            self.class_repo.update(train_class)

        # 4. Generate unique PNR
        pnr = generate_pnr()
        while self.ticket_repo.get_by_pnr(pnr) is not None:
            pnr = generate_pnr()

        # 5. Create Ticket record
        ticket = Ticket(
            pnr_number=pnr,
            user_id=user_id,
            train_id=train_class.train_id,
            train_class_id=train_class.id,
            passenger_id=passenger_id,
            journey_date=dto.journey_date,
            coach_number=coach,
            seat_number=seat,
            ticket_status=status,
        )
        self.ticket_repo.create(ticket)
        self.db.flush()

        # 6. Initialize Payment in PENDING status
        payment = Payment(
            ticket_id=ticket.id,
            amount=train_class.fare,
            payment_status=PaymentStatus.PENDING,
            transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
        )
        self.db.add(payment)
        self.db.commit()

        # Fetch loaded ticket with relationships
        full_ticket = self.ticket_repo.get_by_pnr(pnr)
        return TicketResponseDto.model_validate(full_ticket)

    def cancel_ticket(self, ticket_id: int, user_id: int) -> TicketCancelResponseDto:
        ticket = self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundException("Ticket not found")

        if ticket.user_id != user_id:
            raise ForbiddenException("You can only cancel your own tickets")

        if ticket.ticket_status == TicketStatus.CANCELLED:
            raise BadRequestException("Ticket is already cancelled")

        prev_status = ticket.ticket_status
        freed_coach = ticket.coach_number
        freed_seat = ticket.seat_number

        # 1. Update ticket to CANCELLED
        ticket.ticket_status = TicketStatus.CANCELLED
        self.ticket_repo.update(ticket)

        # 2. Queue Promotion (WAITING/RAC promotion)
        if prev_status == TicketStatus.BOOKED:
            # Check if any RAC ticket exists to promote to BOOKED
            rac_ticket = self.ticket_repo.get_next_in_queue(
                ticket.train_class_id, ticket.journey_date, TicketStatus.RAC
            )
            if rac_ticket:
                # RAC promoted to BOOKED, gets the freed seat
                rac_ticket.ticket_status = TicketStatus.BOOKED
                rac_ticket.coach_number = freed_coach
                rac_ticket.seat_number = freed_seat
                self.ticket_repo.update(rac_ticket)

                # Check if any WAITING ticket can now be promoted to RAC
                wl_ticket = self.ticket_repo.get_next_in_queue(
                    ticket.train_class_id, ticket.journey_date, TicketStatus.WAITING
                )
                if wl_ticket:
                    wl_ticket.ticket_status = TicketStatus.RAC
                    wl_ticket.coach_number = "RAC"
                    wl_ticket.seat_number = "RAC-1"
                    self.ticket_repo.update(wl_ticket)
            else:
                # If no RAC, check if direct WAITING ticket exists
                wl_ticket = self.ticket_repo.get_next_in_queue(
                    ticket.train_class_id, ticket.journey_date, TicketStatus.WAITING
                )
                if wl_ticket:
                    wl_ticket.ticket_status = TicketStatus.BOOKED
                    wl_ticket.coach_number = freed_coach
                    wl_ticket.seat_number = freed_seat
                    self.ticket_repo.update(wl_ticket)
                else:
                    # No waiting list, restore available seats on TrainClass
                    train_class = self.class_repo.get_with_lock(ticket.train_class_id)
                    if train_class:
                        train_class.available_seats = min(
                            train_class.total_seats, train_class.available_seats + 1
                        )
                        self.class_repo.update(train_class)

        # 3. Commit changes
        self.db.commit()

        fare_amount = float(ticket.payment.amount) if ticket.payment else 0.0
        return TicketCancelResponseDto(
            ticket_id=ticket.id,
            pnr_number=ticket.pnr_number,
            previous_status=prev_status,
            new_status=TicketStatus.CANCELLED,
            seat_released=f"{freed_coach}-{freed_seat}" if freed_seat else None,
            refund_status="REFUND_SUCCESSFUL",
            refund_amount=fare_amount,
        )

    def get_ticket_by_pnr(self, pnr: str) -> TicketResponseDto:
        ticket = self.ticket_repo.get_by_pnr(pnr)
        if not ticket:
            raise NotFoundException(f"No ticket found for PNR '{pnr}'")
        return TicketResponseDto.model_validate(ticket)

    def get_all_tickets(self, user_id: int, skip: int = 0, limit: int = 50) -> List[TicketResponseDto]:
        tickets = self.ticket_repo.get_user_tickets(user_id, skip=skip, limit=limit)
        return [TicketResponseDto.model_validate(t) for t in tickets]
