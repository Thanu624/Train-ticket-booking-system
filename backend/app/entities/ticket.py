from sqlalchemy import Column, String, Date, Integer, BigInteger, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity
from app.enums import TicketStatus


class Ticket(BaseEntity):
    __tablename__ = "tickets"

    pnr_number = Column(String(20), unique=True, index=True, nullable=False)
    user_id = Column(Integer().with_variant(BigInteger, "mysql"), ForeignKey("users.id"), nullable=False, index=True)
    train_id = Column(Integer().with_variant(BigInteger, "mysql"), ForeignKey("trains.id"), nullable=False, index=True)
    train_class_id = Column(Integer().with_variant(BigInteger, "mysql"), ForeignKey("train_classes.id"), nullable=False, index=True)
    passenger_id = Column(Integer().with_variant(BigInteger, "mysql"), ForeignKey("passengers.id"), nullable=False, index=True)
    journey_date = Column(Date, nullable=False, index=True)
    seat_number = Column(String(20), nullable=True)
    coach_number = Column(String(20), nullable=True)
    ticket_status = Column(SqlEnum(TicketStatus), default=TicketStatus.BOOKED, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="tickets")
    train = relationship("Train", back_populates="tickets")
    train_class = relationship("TrainClass", back_populates="tickets")
    passenger = relationship("Passenger", back_populates="tickets")
    payment = relationship("Payment", back_populates="ticket", uselist=False, cascade="all, delete-orphan")
