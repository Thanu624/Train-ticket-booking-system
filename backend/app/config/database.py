import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

logger = logging.getLogger(__name__)


def create_db_engine():
    is_testing = os.getenv("TESTING") == "1" or settings.APP_ENV == "testing"
    if is_testing:
        return create_engine(
            "sqlite:///./test_train_booking.db",
            connect_args={"check_same_thread": False},
            echo=False,
        )

    if settings.USE_SQLITE:
        logger.info("Using SQLite database storage.")
        return create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False},
            echo=False,
        )

    try:
        logger.info("Connecting to MySQL...")
        eng = create_engine(
            settings.DATABASE_URL,
            connect_args={"connect_timeout": 2},
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False,
        )
        with eng.connect() as conn:
            pass
        return eng
    except Exception as e:
        logger.warning(f"MySQL unavailable ({e}). Falling back to SQLite.")
        return create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False},
            echo=False,
        )


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that yields a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
