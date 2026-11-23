from sqlalchemy import Column, String, Numeric, Integer, BigInteger, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity
from app.enums import PaymentStatus


class Payment(BaseEntity):
    __tablename__ = "payments"

    ticket_id = Column(
        Integer().with_variant(BigInteger, "mysql"),
        ForeignKey("tickets.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)
    transaction_id = Column(String(64), unique=True, nullable=False)

    # Relationships
    ticket = relationship("Ticket", back_populates="payment")
