from abc import ABC, abstractmethod
from typing import List
from app.dtos.ticket_dto import TicketRequestDto, TicketResponseDto, TicketCancelResponseDto


class ITicketService(ABC):
    @abstractmethod
    def book_ticket(self, user_id: int, dto: TicketRequestDto) -> TicketResponseDto:
        pass

    @abstractmethod
    def cancel_ticket(self, ticket_id: int, user_id: int) -> TicketCancelResponseDto:
        pass

    @abstractmethod
    def get_ticket_by_pnr(self, pnr: str) -> TicketResponseDto:
        pass

    @abstractmethod
    def get_all_tickets(self, user_id: int, skip: int = 0, limit: int = 50) -> List[TicketResponseDto]:
        pass
