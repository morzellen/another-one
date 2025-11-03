from datetime import datetime
from uuid import UUID

from ...errors import BookingCannotBeCompleted, BookingTimeRangeCannotBeEmpty
from ..value_objects.time_range import TimeRange
from ..enums import (
    BookingStatusesEnum,
    PaymentMethodsEnum,
    PaymentStatusesEnum,
    ServicesTypesEnum,
)
from ..constants import BOOKING_ALLOWED_SERVICES


class Booking:
    """
    This class represents a studio booking in the recording studio management platform.
    Bookings are used to schedule services for clients, such as mixing,
    mastering, recording and etc.
    It can be created by clients and confirmed by studio owners.
    It can be linked to an existing project and its subprojects, or not linked at all.
    Client can reschedule the booking by himself, but only if it is confirmed by
    the owner/the person responsible for it. Otherwise, he may return to the time that
    was agreed upon.
    Note:
        The `service_type` must be one of the services allowed for booking.
        See `BOOKING_ALLOWED_SERVICES` for the valid options.
    """

    # region Constructor
    def __init__(
        self,
        id: UUID,
        studio_id: UUID,
        client_id: UUID,
        assigned_employee_id: UUID,
        service_type: ServicesTypesEnum,
        time_range: TimeRange,
        created_at: datetime,
        confirmed_at: datetime | None = None,
        cancelled_at: datetime | None = None,
        completed_at: datetime | None = None,
        rescheduled_at: datetime | None = None,
        project_id: UUID | None = None,
        status: BookingStatusesEnum = BookingStatusesEnum.CREATED,
        payment_status: PaymentStatusesEnum = PaymentStatusesEnum.PENDING,
        payment_method: PaymentMethodsEnum = PaymentMethodsEnum.CASH,
    ):
        self._validate_service_type(service_type)
        self._validate_time_range(time_range)
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
        self._project_id = project_id
        self._status = status
        self._payment_status = payment_status
        self._payment_method = payment_method

    def _validate_service_type(self, service_type: ServicesTypesEnum) -> None:
        """Validate that the service_type is allowed for booking."""
        if service_type not in BOOKING_ALLOWED_SERVICES:
            raise ValueError(
                f"Service '{service_type.value}' is not allowed for booking. "
                f"Allowed services: {[service.value for service in BOOKING_ALLOWED_SERVICES]}"
            )

    def _validate_time_range(self, time_range: TimeRange) -> None:
        """Validate that the time_range is not in the past."""
        if time_range.end_time is None:
            raise BookingTimeRangeCannotBeEmpty(
                "Booking time range cannot be empty. Please provide a start and an end time."
            )

    # endregion

    # region Properties
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
    def service_type(self) -> ServicesTypesEnum:
        return self._service_type

    @property
    def time_range(self) -> TimeRange:
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
    def payment_status(self) -> PaymentStatusesEnum:
        return self._payment_status

    @property
    def payment_method(self) -> PaymentMethodsEnum:
        return self._payment_method

    @property
    def is_active(self) -> bool:
        """Проверяет, активно ли бронирование."""
        return self._status in (
            BookingStatusesEnum.CREATED,
            BookingStatusesEnum.CONFIRMED,
            BookingStatusesEnum.RESCHEDULED,
        )

    @property
    def can_be_confirmed(self) -> bool:
        """Можно подтвердить ТОЛЬКО новые или перенесённые брони."""
        return self._status in (BookingStatusesEnum.CREATED, BookingStatusesEnum.RESCHEDULED)

    @property
    def can_be_rescheduled(self) -> bool:
        """Можно перенести, если бронь активна И не превышён лимит переносов."""
        if not self.is_active:
            return False
        # Бизнес-правило: не более 2 переносов
        return self._reschedule_count < 2

    @property
    def can_be_cancelled(self) -> bool:
        """
        Проверяет, можно ли отменить бронирование.
        """
        return self.is_active

    @property
    def can_be_completed(self) -> bool:
        """
        Проверяет, можно ли завершить бронирование.
        """
        return self._status == BookingStatusesEnum.CONFIRMED

    # endregion

    # region Methods
    def confirm(self, confirmed_at: datetime):
        """Подтверждает бронирование."""
        if self._status != BookingStatusesEnum.CREATED:
            raise ValueError("Cannot confirm booking that is not in CREATED status")
        self._status = BookingStatusesEnum.CONFIRMED
        self._confirmed_at = confirmed_at

    def cancel(self, cancelled_at: datetime):
        """Отменяет бронирование."""
        if self._status == BookingStatusesEnum.COMPLETED:
            raise ValueError("Cannot cancel completed booking")
        self._status = BookingStatusesEnum.CANCELLED
        self._cancelled_at = cancelled_at

    def complete(self, completed_at: datetime):
        """Завершает бронирование."""
        if not self.can_be_completed:
            raise BookingCannotBeCompleted("Cannot complete booking that is not confirmed")
        self._status = BookingStatusesEnum.COMPLETED
        self._completed_at = completed_at

    def reschedule(self, new_time_range: TimeRange, rescheduled_at: datetime):
        """Переносит бронирование."""
        if self._status not in [BookingStatusesEnum.CREATED, BookingStatusesEnum.CONFIRMED]:
            raise ValueError("Cannot reschedule booking that is cancelled or completed")
        self._time_range = new_time_range
        self._rescheduled_at = rescheduled_at
        if self.can_be_confirmed:
            self._status = BookingStatusesEnum.RESCHEDULED

    def update_payment_status(self, payment_status: PaymentStatusesEnum):
        """Обновляет статус оплаты."""
        self._payment_status = payment_status

    def has_conflict_with_time_range(self, other_time_range: TimeRange) -> bool:
        """Проверяет, конфликтует ли это бронирование с другим временным диапазоном."""
        return (
            self._time_range.start_time < other_time_range.end_time
            and self._time_range.end_time > other_time_range.start_time
        )

    def is_past(self, current_time: datetime) -> bool:
        """
        Проверяет, прошло ли бронирование на основе переданного времени.
        """
        return self._time_range.end_time < current_time

    def is_confirmed_and_active(self, current_time: datetime) -> bool:
        """
        Проверяет, подтверждено ли бронирование и активно ли оно в данный момент.
        """
        return self._status == BookingStatusesEnum.CONFIRMED and not self.is_past(current_time)

    # endregion
