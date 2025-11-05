from dataclasses import dataclass
from datetime import datetime, timedelta
from src.errors import InvalidBookingTimeRangeError


@dataclass(frozen=True)
class BookingTimeRange:
    """
    Value Object для временных диапазонов бронирования (всегда ограниченные).

    Бизнес-правила:
    - Должны быть определены start_time и end_time
    - end_time должен быть строго позже start_time
    - Используется исключительно в контексте сущности Booking

    Пример:
        recording_session = BookingTimeRange(
            start_time=datetime(2024, 1, 15, 14, 0),
            end_time=datetime(2024, 1, 15, 16, 30)
        )
    """

    start_time: datetime
    end_time: datetime

    def __post_init__(self):
        """Проверяет инварианты временного диапазона."""
        if self.end_time <= self.start_time:
            raise InvalidBookingTimeRangeError(
                f"Некорректный временной диапазон бронирования: end_time ({self.end_time}) "
                f"должен быть позже start_time ({self.start_time})"
            )
        if self.start_time.tzinfo is None or self.end_time.tzinfo is None:
            raise ValueError("Требуются даты и время с информацией о часовом поясе")

    def contains(self, time: datetime) -> bool:
        """
        Проверяет, попадает ли указанное время в этот диапазон бронирования.

        :param time: Время для проверки
        :return: True если время находится внутри [start_time, end_time]
        """
        return self.start_time <= time <= self.end_time

    def overlaps_with(self, other: "BookingTimeRange") -> bool:
        """
        Проверяет, пересекается ли этот временной диапазон с другим.

        Обрабатываемые крайние случаи:
        - [10:00-12:00] пересекается с [11:00-13:00] → True
        - [10:00-12:00] пересекается с [12:00-13:00] → False (конец исключается)
        - [10:00-12:00] пересекается с [09:00-10:00] → False

        :param other: Другой временной диапазон для проверки
        :return: True если диапазоны имеют общие точки времени
        """
        return self.start_time < other.end_time and self.end_time > other.start_time

    def duration(self) -> timedelta:
        """Вычисляет продолжительность временного диапазона."""
        return self.end_time - self.start_time

    def __str__(self) -> str:
        """Человекочитаемое представление для логов и UI."""
        return (
            f"{self.start_time.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.end_time.strftime('%Y-%m-%d %H:%M')}"
        )

    def __repr__(self) -> str:
        """Техническое представление для отладки."""
        return (
            f"BookingTimeRange("
            f"start_time={self.start_time.isoformat()}, "
            f"end_time={self.end_time.isoformat()})"
        )
