class BookingCannotBeConfirmedError(Exception):
    DEFAULT_MESSAGE = "Бронирование в статусе {status} не может быть подтверждено"

    def __init__(self, status: str):
        super().__init__(self.DEFAULT_MESSAGE.format(status=status.value))


class BookingCannotBeCanceledError(Exception):
    DEFAULT_MESSAGE = "Бронирование не может быть отменено"
    CANCELLED_BOOKING_MESSAGE = (
        "Невозможно отменить бронирование {id}. Либо неактивно, либо в течение периода отмены"
    )

    def __init__(self, message_template: str = None, id: int | None = None):
        message = (
            message_template or self.DEFAULT_MESSAGE or self.CANCELLED_BOOKING_MESSAGE.format(id=id)
        )
        super().__init__(message)


class BookingCannotBeCompletedError(Exception):
    DEFAULT_MESSAGE = "Нельзя завершить бронирование, которое не подтверждено"

    def __init__(self, message_template: str = None):
        message = message_template or self.DEFAULT_MESSAGE
        super().__init__(message)


class BookingCannotBeRescheduledError(Exception):
    DEFAULT_MESSAGE = (
        "Бронирование не может быть перенесено. "
        "Текущий статус: {status}, количество переносов: {reschedule_count}/{limit}"
    )

    def __init__(self, status: str, reschedule_count: int, limit: int):
        message = self.DEFAULT_MESSAGE.format(
            status=status, reschedule_count=reschedule_count, limit=limit
        )
        super().__init__(message)
