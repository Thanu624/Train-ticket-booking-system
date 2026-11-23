import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

# Path to backend/.env file
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else ".env",
        extra="ignore"
    )

    APP_NAME: str = "Train Ticket Booking System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "super_secret_jwt_key_train_booking_production_ready_key_12345"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Database
    USE_SQLITE: bool = True
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "train_user"
    DB_PASSWORD: str = "train_secure_password_2026"
    DB_NAME: str = "train_booking_db"
    DATABASE_URL: str = "mysql+pymysql://train_user:train_secure_password_2026@localhost:3306/train_booking_db"
    SQLITE_FALLBACK_URL: str = "sqlite:///./train_booking.db"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]


settings = Settings()
