import logging
from uuid import UUID
from datetime import datetime, timedelta

from .value_object.booking_time_range_vo import BookingTimeRange
from .booking_enums import BookingStatusesEnum, BookingServicesTypesEnum
from .booking_events import (
    BookingCancelledEvent,
    BookingCompletedEvent,
    BookingConfirmedEvent,
    BookingRescheduledEvent,
    DomainEvent,
)
from .booking_errors import (
    BookingCannotBeCanceledError,
    BookingCannotBeCompletedError,
    BookingCannotBeConfirmedError,
    BookingCannotBeRescheduledError,
)

logger = logging.getLogger(__name__)


class Booking:
    """
    Этот класс представляет бронирование студии в платформе управления звукозаписывающими студиями.
    Бронирования используются для планирования услуг для клиентов, таких как сведение,
    мастеринг, запись и т.д.
    Может быть создано клиентами и подтверждено владельцами студии.
    Может быть привязано к существующему проекту и его подпроектам или не привязано вообще.
    Клиент может перенести бронирование самостоятельно, но только если оно будет подтверждено
    владельцем/ответственным лицом. В противном случае он может вернуться к изначально
    согласованному времени.
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
    def reschedule_count(self) -> int:
        return self._reschedule_count

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
        return self._rescheduled_at is not None and self._status == BookingStatusesEnum.RESCHEDULED

    @property
    def is_confirmed(self) -> bool:
        """
        Проверяет, подтверждено ли бронирование.
        """
        return self._confirmed_at is not None and self._status == BookingStatusesEnum.CONFIRMED

    @property
    def is_completed(self) -> bool:
        """
        Проверяет, завершено ли бронирование.
        """
        return self._completed_at is not None and self._status == BookingStatusesEnum.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        """
        Проверяет, отменено ли бронирование.
        """
        return self._cancelled_at is not None and self._status == BookingStatusesEnum.CANCELLED

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
        return self.is_active and self._reschedule_count < self.__BOOKING_RESCHEDULE_LIMIT

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

    # region Методы

    def can_be_cancelled(self, current_time: datetime) -> bool:
        """
        Проверяет, можно ли отменить бронирование.
        Бронирование нельзя отменить за 24 часа до начала.
        Если бронирование подтверждено, его тоже можно отменить
        (непредвиденные ситуации на студии, например).

        В application — передача текущего времени через параметр.
        """
        time_until_booking = self.time_range.start_time - current_time
        cancellation_cutoff = timedelta(hours=self.__CANCELLATION_CUTOFF_HOURS)
        return self.is_active and time_until_booking > cancellation_cutoff

    def mark_as_confirmed(self, current_time: datetime) -> list[DomainEvent]:
        """Помечает бронирование как подтвержденное и публикует событие"""
        if not self.can_be_confirmed:
            raise BookingCannotBeConfirmedError(self._status.value)

        self._status = BookingStatusesEnum.CONFIRMED
        self._confirmed_at = current_time

        event = BookingConfirmedEvent(
            occurred_at=self._confirmed_at,
            booking_id=self.id,
            studio_id=self.studio_id,
            client_id=self.client_id,
            time_range_start=self.time_range.start_time,
            time_range_end=self.time_range.end_time,
        )

        logger.info(f"📤 Публикация события подтверждения бронирования: {event.booking_id}")

        return [event]

    def mark_as_cancelled(
        self, current_time: datetime, cancellation_reason: str | None = None
    ) -> list[DomainEvent]:
        """Помечает бронирование как отмененное и публикует событие."""
        if not self.can_be_cancelled(current_time):
            raise BookingCannotBeCanceledError(
                BookingCannotBeCanceledError.CANCELLED_BOOKING_MESSAGE, self._id
            )

        self._status = BookingStatusesEnum.CANCELLED
        self._cancelled_at = current_time

        event = BookingCancelledEvent(
            occurred_at=self._cancelled_at,
            booking_id=self.id,
            studio_id=self.studio_id,
            client_id=self.client_id,
            reason=cancellation_reason,
        )

        logger.info(f"📤 Публикация события отмены бронирования: {event.booking_id}")

        return [event]

    def mark_as_completed(self, current_time: datetime) -> list[DomainEvent]:
        """
        Помечает бронирование как завершенное и публикует событие.
        Оно может быть завершено после того, как время бронирования закончилось.
        """
        if not self.can_be_completed:
            raise BookingCannotBeCompletedError()
        self._status = BookingStatusesEnum.COMPLETED
        self._completed_at = current_time

        event = BookingCompletedEvent(
            occurred_at=self._completed_at,
            booking_id=self.id,
            studio_id=self.studio_id,
            client_id=self.client_id,
        )

        logger.info(f"📤 Публикация события завершения бронирования: {event.booking_id}")

        return [event]

    def mark_as_rescheduled(
        self, new_time_range: BookingTimeRange, current_time: datetime
    ) -> list[DomainEvent]:
        """
        Помечает бронирование как перенесённое и публикует событие. После переноса:
        - Статус меняется на RESCHEDULED (требуется повторное подтверждение)
        - Увеличивается счётчик переносов
        """
        if not self.can_be_rescheduled:
            raise BookingCannotBeRescheduledError(
                status=self._status.value,
                reschedule_count=self._reschedule_count,
                limit=self.__BOOKING_RESCHEDULE_LIMIT,
            )
        self._time_range = new_time_range
        self._reschedule_count += 1
        self._status = BookingStatusesEnum.RESCHEDULED
        self._rescheduled_at = current_time

        event = BookingRescheduledEvent(
            occurred_at=self._rescheduled_at,
            booking_id=self.id,
            studio_id=self.studio_id,
            client_id=self.client_id,
            time_range_start=self.time_range.start_time,
            time_range_end=self.time_range.end_time,
        )

        logger.info(f"📤 Публикация события переноса бронирования: {event.booking_id}")

        return [event]

    # endregion
