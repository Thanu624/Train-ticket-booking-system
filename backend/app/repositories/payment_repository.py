from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.entities.payment import Payment
from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: Session):
        super().__init__(Payment, db)

    def get_by_ticket_id(self, ticket_id: int) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.ticket_id == ticket_id)
        return self.db.scalars(stmt).first()

    def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.transaction_id == transaction_id)
        return self.db.scalars(stmt).first()
