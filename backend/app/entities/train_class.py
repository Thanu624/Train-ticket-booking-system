from sqlalchemy import Column, Integer, BigInteger, Numeric, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.entities.base_entity import BaseEntity
from app.enums import ClassType


class TrainClass(BaseEntity):
    __tablename__ = "train_classes"

    train_id = Column(
        Integer().with_variant(BigInteger, "mysql"),
        ForeignKey("trains.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    class_type = Column(SqlEnum(ClassType), nullable=False)
    fare = Column(Numeric(10, 2), nullable=False)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    # Relationships
    train = relationship("Train", back_populates="train_classes")
    tickets = relationship("Ticket", back_populates="train_class")
