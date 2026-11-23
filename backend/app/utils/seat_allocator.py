from typing import Tuple
from app.enums import ClassType, TicketStatus
from app.constants.app_constants import COACH_PREFIX_MAP, COACH_CAPACITIES


def allocate_coach_and_seat(
    class_type: ClassType,
    confirmed_count: int,
    total_capacity: int,
    waiting_count: int = 0
) -> Tuple[TicketStatus, str, str]:
    """
    Allocates seat status, coach number, and seat number deterministically.
    - If confirmed_count < total_capacity: Status is BOOKED with Coach (e.g. S1, B1) and seat number.
    - If total_capacity <= confirmed_count < total_capacity + rac_limit: Status is RAC.
    - Otherwise: Status is WAITING (WL).
    """
    c_type_str = class_type.value if hasattr(class_type, "value") else str(class_type)
    coach_prefix = COACH_PREFIX_MAP.get(c_type_str, "C")
    coach_capacity = COACH_CAPACITIES.get(c_type_str, 72)

    # 1. Confirmed booking available
    if confirmed_count < total_capacity:
        seat_index = confirmed_count + 1
        coach_num = ((seat_index - 1) // coach_capacity) + 1
        seat_num = ((seat_index - 1) % coach_capacity) + 1
        return TicketStatus.BOOKED, f"{coach_prefix}{coach_num}", str(seat_num)

    # 2. RAC Threshold (up to 10% or minimum 6 seats)
    rac_limit = max(6, int(total_capacity * 0.10))
    rac_current = confirmed_count - total_capacity

    if rac_current < rac_limit:
        rac_number = rac_current + 1
        return TicketStatus.RAC, "RAC", f"RAC-{rac_number}"

    # 3. Waiting List
    wl_number = waiting_count + 1
    return TicketStatus.WAITING, "WL", f"WL-{wl_number}"
