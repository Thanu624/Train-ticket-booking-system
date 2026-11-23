from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func, and_
from app.entities.ticket import Ticket
from app.enums import TicketStatus
from app.repositories.base_repository import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, db: Session):
        super().__init__(Ticket, db)

    def get_by_pnr(self, pnr_number: str) -> Optional[Ticket]:
        stmt = (
            select(Ticket)
            .where(Ticket.pnr_number == pnr_number.strip().upper())
            .options(
                selectinload(Ticket.train),
                selectinload(Ticket.train_class),
                selectinload(Ticket.passenger),
                selectinload(Ticket.payment),
            )
        )
        return self.db.scalars(stmt).first()

    def get_user_tickets(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Ticket]:
        stmt = (
            select(Ticket)
            .where(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(Ticket.train),
                selectinload(Ticket.train_class),
                selectinload(Ticket.passenger),
                selectinload(Ticket.payment),
            )
        )
        return list(self.db.scalars(stmt).all())

    def count_by_status(self, train_class_id: int, journey_date: date, status: TicketStatus) -> int:
        stmt = select(func.count(Ticket.id)).where(
            and_(
                Ticket.train_class_id == train_class_id,
                Ticket.journey_date == journey_date,
                Ticket.ticket_status == status,
            )
        )
        return self.db.scalar(stmt) or 0

    def get_next_in_queue(self, train_class_id: int, journey_date: date, status: TicketStatus) -> Optional[Ticket]:
        """Gets next ticket waiting or RAC in FIFO order with row lock."""
        stmt = (
            select(Ticket)
            .where(
                and_(
                    Ticket.train_class_id == train_class_id,
                    Ticket.journey_date == journey_date,
                    Ticket.ticket_status == status,
                )
            )
            .order_by(Ticket.id.asc())
            .with_for_update()
        )
        return self.db.scalars(stmt).first()
