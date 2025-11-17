from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Базовый класс для всех доменных событий"""

    event_id: UUID
    occurred_at: datetime


@dataclass(frozen=True)
class BookingConfirmedEvent(DomainEvent):
    """Событие подтверждения бронирования"""

    booking_id: UUID
    studio_id: UUID
    client_id: UUID
    time_range_start: datetime
    time_range_end: datetime


@dataclass(frozen=True)
class BookingCancelledEvent(DomainEvent):
    """Событие отмены бронирования"""

    booking_id: UUID
    client_id: UUID
    reason: str
