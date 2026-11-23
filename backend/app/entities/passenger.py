from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity


class Passenger(BaseEntity):
    __tablename__ = "passengers"

    user_id = Column(
        Integer().with_variant(BigInteger, "mysql"),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    mobile_number = Column(String(15), nullable=False)

    # Relationships
    user = relationship("User", back_populates="passengers")
    tickets = relationship("Ticket", back_populates="passenger")
