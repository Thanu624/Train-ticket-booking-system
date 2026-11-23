from abc import ABC, abstractmethod
from app.dtos.payment_dto import PaymentProcessDto, PaymentResponseDto


class IPaymentService(ABC):
    @abstractmethod
    def process_payment(self, user_id: int, dto: PaymentProcessDto) -> PaymentResponseDto:
        pass

    @abstractmethod
    def get_payment_by_ticket(self, ticket_id: int) -> PaymentResponseDto:
        pass
