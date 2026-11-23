"""Application constants and regex patterns"""

MOBILE_REGEX = r"^\+?[1-9]\d{9,14}$"
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Seat Allocation Rules
COACH_PREFIX_MAP = {
    "1A": "H",
    "2A": "A",
    "3A": "B",
    "SL": "S",
    "CC": "C",
    "EC": "E",
    "2S": "D",
    "GN": "GS",
}

COACH_CAPACITIES = {
    "1A": 24,
    "2A": 54,
    "3A": 72,
    "SL": 72,
    "CC": 75,
    "EC": 56,
    "2S": 108,
    "GN": 100,
}

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100
