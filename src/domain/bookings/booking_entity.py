from uuid import UUID
from datetime import datetime, timedelta

from .value_objects.booking_time_range_vo import BookingTimeRange
from .booking_enums import BookingStatusesEnum, BookingServicesTypesEnum
from .booking_errors import (
    BookingCannotBeCanceledError,
    BookingCannotBeCompletedError,
    BookingCannotBeConfirmedError,
    BookingCannotBeRescheduledError,
)


class Booking:
    """
    Этот класс представляет бронирование студии в платформе управления звукозаписывающими студиями.
    Бронирования используются для планирования услуг для клиентов, таких как сведение,
    мастеринг, запись и т.д.
    Может быть создано клиентами и подтверждено владельцами студии.
    Может быть привязано к существующему проекту и его подпроектам или не привязано вообще.
    Клиент может перенести бронирование самостоятельно, но только если оно подтверждено
    владельцем/ответственным лицом. В противном случае он может вернуться к изначально
    согласованному времени.
    Примечание:
        `service_type` должен быть одной из услуг, разрешённых для бронирования.
        См. `BOOKING_ALLOWED_SERVICES` для допустимых вариантов.
    """

    # region Константы

    # Максимальное количество раз, на которое можно перенести бронирование.
    __BOOKING_RESCHEDULE_LIMIT = 2

    # Часы до начала бронирования, после которых нельзя отменить
    __CANCELLATION_CUTOFF_HOURS = 24

    # endregion

    # region Конструктор
    def __init__(
        self,
        id: UUID,
        studio_id: UUID,
        client_id: UUID,
        payment_id: UUID,  # TODO: убрать здесь, реализовать через События домена + Сервисы домена
        assigned_employee_id: UUID,
        service_type: BookingServicesTypesEnum,
        time_range: BookingTimeRange,
        created_at: datetime,
        confirmed_at: datetime | None = None,
        cancelled_at: datetime | None = None,
        completed_at: datetime | None = None,
        rescheduled_at: datetime | None = None,
        project_id: UUID | None = None,
        status: BookingStatusesEnum = BookingStatusesEnum.CREATED,
    ):
        self._id = id
        self._studio_id = studio_id
        self._client_id = client_id
        self._assigned_employee_id = assigned_employee_id
        self._service_type = service_type
        self._time_range = time_range
        self._created_at = created_at
        self._confirmed_at = confirmed_at
        self._cancelled_at = cancelled_at
        self._completed_at = completed_at
        self._rescheduled_at = rescheduled_at
        self._reschedule_count = 0
        self._project_id = project_id
        self._status = status

    # endregion

    # region Свойства
    @property
    def id(self) -> UUID:
        return self._id

    @property
    def studio_id(self) -> UUID:
        return self._studio_id

    @property
    def client_id(self) -> UUID:
        return self._client_id

    @property
    def assigned_employee_id(self) -> UUID:
        return self._assigned_employee_id

    @property
    def service_type(self) -> BookingServicesTypesEnum:
        return self._service_type

    @property
    def time_range(self) -> BookingTimeRange:
        return self._time_range

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def confirmed_at(self) -> datetime | None:
        return self._confirmed_at

    @property
    def cancelled_at(self) -> datetime | None:
        return self._cancelled_at

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    @property
    def rescheduled_at(self) -> datetime | None:
        return self._rescheduled_at

    @property
    def project_id(self) -> UUID | None:
        return self._project_id

    @property
    def status(self) -> BookingStatusesEnum:
        return self._status

    @property
    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование."""
        return self._status in (
            BookingStatusesEnum.CREATED,
            BookingStatusesEnum.RESCHEDULED,
            BookingStatusesEnum.CONFIRMED,
        )

    @property
    def is_created(self) -> bool:
        """
        Проверяет, ожидает ли бронирование подтверждения.
        """
        return self._status == BookingStatusesEnum.CREATED

    @property
    def is_rescheduled(self) -> bool:
        """
        Проверяет, перенесено ли бронирование.
        """
        return self._status == BookingStatusesEnum.RESCHEDULED

    @property
    def is_confirmed(self) -> bool:
        """
        Проверяет, подтверждено ли бронирование.
        """
        return self._status == BookingStatusesEnum.CONFIRMED

    @property
    def is_completed(self) -> bool:
        """
        Проверяет, завершено ли бронирование.
        """
        return self._status == BookingStatusesEnum.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        """
        Проверяет, отменено ли бронирование.
        """
        return self._status == BookingStatusesEnum.CANCELLED

    @property
    def is_pending(self) -> bool:
        """
        Проверяет, ожидает ли бронирование подтверждения.
        Ожидание - состояние созданных и перенесённых бронирований.
        """
        return self.is_created or self.is_rescheduled

    @property
    def can_be_confirmed(self) -> bool:
        """Можно подтвердить бронь только если она ожидается."""
        return self.is_pending

    @property
    def can_be_rescheduled(self) -> bool:
        """
        Можно перенести, если:
        - бронь активна (CREATED/RESCHEDULED/CONFIRMED),
        - не превышен лимит переносов
        TODO:
        Добавить проверку, что время бронирования не пересекается с другими бронированиями.
        Если мы добавим эту проверку, то теоретически это становится методом, а не свойством.
        """
        return self.is_active and self._reschedule_count < self.reschedule_limit

    @property
    def can_be_completed(self) -> bool:
        """
        Проверяет, можно ли завершить бронирование.
        """
        return self.is_confirmed

    @property
    def reschedule_limit(self) -> int:
        return self.__BOOKING_RESCHEDULE_LIMIT

    @property
    def cancellation_cutoff_hours(self) -> int:
        return self.__CANCELLATION_CUTOFF_HOURS

    # endregion

    # region
    # Методы TODO: вынести строковые сообщения в классы ошибок;
    # TODO: Нужно проверять на конфликты с другими временными диапозонами бронирований (с другими бронированиями)
    # в can_be_confirmed, can_be_rescheduled, поскольку они отвечают на вопрос о том, можно ли подтвердить
    # или перенести. Значит они точно не будут свойствами. У нас есть booking_conflict_checker_service.py

    def can_be_cancelled(self, current_time: datetime) -> bool:
        """
        Проверяет, можно ли отменить бронирование.
        Бронирование нельзя отменить за 24 часа до начала.
        Если бронирование подтверждено, его тоже можно отменить
        (непредвиденные ситуации на студии, например).

        В application — передача текущего времени через параметр.

        TODO: Подумать над timedelta(hours=self.cancellation_cutoff_hours)
        """
        time_until_booking = self.time_range.start_time - current_time
        is_within_cutoff = time_until_booking < timedelta(hours=self.cancellation_cutoff_hours)
        return self.is_active and not is_within_cutoff

    def confirm(self, confirmed_at: datetime):
        """Подтверждает бронирование."""
        if not self.can_be_confirmed:
            raise BookingCannotBeConfirmedError(self._status)
        self._status = BookingStatusesEnum.CONFIRMED
        self._confirmed_at = confirmed_at

    def cancel(self, cancelled_at: datetime):
        """Отменяет бронирование."""
        if self._status == BookingStatusesEnum.COMPLETED:
            raise BookingCannotBeCanceledError(
                BookingCannotBeCanceledError.COMPLETED_BOOKING_MESSAGE
            )
        self._status = BookingStatusesEnum.CANCELLED
        self._cancelled_at = cancelled_at

    def complete(self, completed_at: datetime):
        """
        Завершает бронирование.
        Оно может быть завершено после того, как время бронирования закончилось.
        """
        if not self.can_be_completed:
            raise BookingCannotBeCompletedError()
        self._status = BookingStatusesEnum.COMPLETED
        self._completed_at = completed_at

    def reschedule(self, new_time_range: BookingTimeRange, rescheduled_at: datetime):
        """
        Переносит бронирование. После переноса:
        - Статус меняется на RESCHEDULED (требуется повторное подтверждение)
        - Увеличивается счётчик переносов
        """
        if not self.can_be_rescheduled:
            raise BookingCannotBeRescheduledError(
                status=self.status,
                reschedule_count=self._reschedule_count,
                limit=self.reschedule_limit,
            )
        self._time_range = new_time_range
        self._rescheduled_at = rescheduled_at
        self._reschedule_count += 1
        self._status = BookingStatusesEnum.RESCHEDULED

    # endregion
