from uuid import UUID
from datetime import datetime

from .value_objects.booking_time_range_vo import BookingTimeRange
from .booking_enums import BookingStatusesEnum, BookingServicesTypesEnum
from .booking_errors import (
    BookingCannotBeCanceledError,
    BookingCannotBeCompletedError,
    BookingCannotBeConfirmedError,
    BookingCannotBeRescheduledError,
    UnsupportedBookingServiceError,
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
    # TODO: подумать, как обезопаситься от случайного изменения этого значения
    _BOOKING_RESCHEDULE_LIMIT = 2

    # endregion

    # region Конструктор
    def __init__(
        self,
        id: UUID,
        studio_id: UUID,
        client_id: UUID,
        payment_id: UUID,  # TODO: будет ли id обязательным? Должно ли тут оно быть?
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
        self._validate_booking_service_type(service_type)
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

    # TODO: Надо ли оно нам здесь? И вообще, BookingServicesTypesEnum это enum
    # TODO: строковое представление ошибки перенести куда-то, если валидация в итоге нужна
    def _validate_booking_service_type(self, service_type: BookingServicesTypesEnum) -> None:
        """Проверяет, что service_type разрешён для бронирования."""
        if service_type not in BookingServicesTypesEnum:
            raise UnsupportedBookingServiceError(
                f"Услуга '{service_type.value}' не разрешена для бронирования. "
                f"Разрешённые услуги: {[service.value for service in BookingServicesTypesEnum]}"
            )

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
        return self.is_active and self._reschedule_count < self._BOOKING_RESCHEDULE_LIMIT

    @property
    def can_be_cancelled(self) -> bool:
        """
        Проверяет, можно ли отменить бронирование.
        TODO:
        Добавить проверку, что бронирование нельзя отменить за 24 часа до начала.
        Не использовать datetime.now() здесь. Принимать текущее время извне.
        Если мы добавим эту проверку, то теоретически это становится методом, а не свойством.
        Если бронирование подтверждено, его тоже можно отменить (непредвиденные ситуации на студии, например).
        """
        return self.is_active

    @property
    def can_be_completed(self) -> bool:
        """
        Проверяет, можно ли завершить бронирование.
        """
        return self.is_confirmed

    # endregion

    # region Методы TODO: вынести строковые сообщения куда-то;
    # TODO: Подумать о внедрении has_conflict_with_other_time_range (если такой метод в итоге оставляем в сущности)
    # в некоторые методы, а скорее даже в properties, такие как can_be_confirmed, can_be_rescheduled,
    # поскольку они отвечают на вопрос о том, можно ли подтвердить или перенести. В таком случае, судя по всему,
    # can_be_confirmed, can_be_rescheduled станут методами, а не свойствами.

    def confirm(self, confirmed_at: datetime):
        """Подтверждает бронирование."""
        if not self.can_be_confirmed:
            raise BookingCannotBeConfirmedError(
                f"Бронирование в статусе {self._status} не может быть подтверждено"
            )
        self._status = BookingStatusesEnum.CONFIRMED
        self._confirmed_at = confirmed_at

    def cancel(self, cancelled_at: datetime):
        """Отменяет бронирование."""
        if self._status == BookingStatusesEnum.COMPLETED:
            raise BookingCannotBeCanceledError("Нельзя отменить завершённое бронирование")
        self._status = BookingStatusesEnum.CANCELLED
        self._cancelled_at = cancelled_at

    def complete(self, completed_at: datetime):
        """
        Завершает бронирование.
        Оно может быть завершено после того, как время бронирования закончилось.
        """
        if not self.can_be_completed:
            raise BookingCannotBeCompletedError(
                "Нельзя завершить бронирование, которое не подтверждено"
            )
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
                f"Бронирование не может быть перенесено. "
                f"Текущий статус: {self.status.value}, "
                f"количество переносов: {self._reschedule_count}/{self._BOOKING_RESCHEDULE_LIMIT}"
            )
        self._time_range = new_time_range
        self._rescheduled_at = rescheduled_at
        self._reschedule_count += 1
        self._status = BookingStatusesEnum.RESCHEDULED

    # TODO: подумать, надо оно тут или нет
    def has_conflict_with_other_time_range(self, other_time_range: BookingTimeRange) -> bool:
        """
        Проверяет, конфликтует ли это бронирование с другим временным диапазоном.
        """
        return self._time_range.overlaps_with(other_time_range)

    # endregion
