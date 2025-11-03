from datetime import datetime
from ..errors import InvalidTimeRangeError


class TimeRange:
    """
    Value Object. Represents the time range, which is part of booking or subscription.
    Value Object должен быть неизменяемым.
    """

    def __init__(self, start_time: datetime, end_time: datetime | None):
        if end_time is not None and end_time <= start_time:
            raise InvalidTimeRangeError("TimeRange must have end_time > start_time")
        self._start_time = start_time
        self._end_time = end_time

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime | None:
        return self._end_time

    def __eq__(self, other) -> bool:
        if not isinstance(other, TimeRange):
            return False
        return self._start_time == other._start_time and self._end_time == other._end_time

    def __hash__(self) -> int:
        return hash((self._start_time, self._end_time))

    def contains(self, time: datetime) -> bool:
        """Checks if the time range contains a specific time."""
        if self._end_time is None:
            return time >= self._start_time
        return self._start_time <= time <= self._end_time

    def overlaps_with(self, other: "TimeRange") -> bool:
        """Checks if this time range overlaps with another time range."""
        if self._end_time is None or other._end_time is None:
            # If either range is open-ended, they overlap if start of one is within the other
            if self._end_time is None:
                return other._start_time <= self._start_time
            else:
                return self._start_time <= other._start_time
        return self._start_time < other._end_time and self._end_time > other._start_time
