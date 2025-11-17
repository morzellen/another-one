from datetime import datetime


class InvalidBookingTimeRangeError(Exception):
    DEFAULT_MESSAGE = "Некорректный временной диапазон бронирования: Конечное время ({end_time}) должно быть позже начального времени ({start_time})"

    def __init__(self, end_time: datetime, start_time: datetime):
        super().__init__(self.DEFAULT_MESSAGE.format(end_time=end_time, start_time=start_time))


class InvalidBookingTimezoneError(Exception):
    DEFAULT_MESSAGE = "Требуются даты и время с информацией о часовом поясе"

    def __init__(self):
        super().__init__(self.DEFAULT_MESSAGE)
