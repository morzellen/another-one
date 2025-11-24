from .value_object.booking_time_range_vo import BookingTimeRange


class BookingConflictChecker:
    @staticmethod
    def has_conflicts(
        target_range: BookingTimeRange, existing_ranges: list[BookingTimeRange]
    ) -> bool:
        """
        Проверяет, конфликтует ли это бронирование с другим временным диапазоном.
        Использовать в application при проверке возможности переноса/подтверждения.
        """
        return any(target_range.overlaps_with(range) for range in existing_ranges)
