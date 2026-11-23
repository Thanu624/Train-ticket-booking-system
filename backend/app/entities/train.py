from sqlalchemy import Column, String, Time
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity


class Train(BaseEntity):
    __tablename__ = "trains"

    train_number = Column(String(20), unique=True, index=True, nullable=False)
    train_name = Column(String(100), nullable=False)
    source = Column(String(80), index=True, nullable=False)
    destination = Column(String(80), index=True, nullable=False)
    departure_time = Column(String(10), nullable=False)  # stored as HH:MM format
    arrival_time = Column(String(10), nullable=False)    # stored as HH:MM format

    # Relationships
    train_classes = relationship("TrainClass", back_populates="train", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="train")
