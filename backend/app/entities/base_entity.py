from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, DateTime
from app.config.database import Base


class BaseEntity(Base):
    __abstract__ = True

    id = Column(
        Integer().with_variant(BigInteger, "mysql"),
        primary_key=True,
        index=True,
        autoincrement=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
