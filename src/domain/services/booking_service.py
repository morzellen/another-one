from datetime import datetime
from typing import Optional
from uuid import UUID

from ..entities.booking import Booking
from ..enums import BookingStatusesEnum
from ..bookings.value_objects.booking_time_range_vo import TimeRange


class BookingDomainService:
    """
    Domain Service для бизнес-логики, связанной с бронированиями.
    """

    @staticmethod
    def calculate_duration_minutes(booking: Booking) -> int:
        """
        Рассчитывает продолжительность бронирования в минутах.
        """
        if booking.time_range.end_time is None:
            return 0
        duration = booking.time_range.end_time - booking.time_range.start_time
        return int(duration.total_seconds() / 60)
