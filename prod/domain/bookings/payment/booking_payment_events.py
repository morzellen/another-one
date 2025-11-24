from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DomainEvent:
    """Базовый класс для всех доменных событий"""

    event_id: UUID = uuid4()  # TODO: Можно ли здесь использовать uuid4()?
    occurred_at: datetime


@dataclass(frozen=True)
class BookingPaymentPaidEvent(DomainEvent):
    """Событие оплаты бронирования"""

    payment_id: UUID
    amount: float


@dataclass(frozen=True)
class BookingPaymentFailedEvent(DomainEvent):
    """Событие неудачной оплаты бронирования"""

    payment_id: UUID
    amount: float


@dataclass(frozen=True)
class BookingPaymentRefundedEvent(DomainEvent):
    """Событие возврата оплаты бронирования"""

    payment_id: UUID
    amount: float
    refunded_reason: str | None
