from sqlalchemy import Column, String, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity
from app.enums import UserRole


class User(BaseEntity):
    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)

    # Relationships
    passengers = relationship("Passenger", back_populates="user", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="user")
