from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class ClassType(str, Enum):
    GN = "GN"  # General
    TWO_S = "2S"  # Second Sitting
    SL = "SL"  # Sleeper Class
    THREE_A = "3A"  # AC 3 Tier
    TWO_A = "2A"  # AC 2 Tier
    ONE_A = "1A"  # AC First Class
    CC = "CC"  # AC Chair Car
    EC = "EC"  # Exec. Chair Car


class TicketStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    WAITING = "WAITING"
    RAC = "RAC"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
