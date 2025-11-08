from enum import StrEnum, auto, unique


@unique
class BookingStatusesEnum(StrEnum):
    """
    This class represents the different statuses that a booking can have throughout its lifecycle.
    These statuses track the progress and state of studio bookings.

    The statuses are as follows:
    - CREATED: The booking has been created and is pending confirmation.
    - RESCHEDULED: The booking has been rescheduled.
    - CONFIRMED: The booking has been confirmed and is scheduled to take place.
    - COMPLETED: The booking has been completed.
    - CANCELLED: The booking has been cancelled.
    """

    CREATED = auto()
    CONFIRMED = auto()
    CANCELLED = auto()
    COMPLETED = auto()
    RESCHEDULED = auto()


@unique
class BookingServicesTypesEnum(StrEnum):
    """
    Эти услуги могут быть выбраны клиентами при создании бронирований.

    Услуги:
        MIXING: Работа со звучанием музыки.
        MASTERING: Работа над финальной версией звучания музыки.
        BEATMAKING: Написание битов для клиента, если он тоже хочет учавствовать в процессе.
        PROMOTION: Реклама и продвижение, совместный мозговой штурм, обсуждение и так далее. Работа над промо-материалами.
        RECORDING: Звукозапись.
        DESIGNING: Дизайн обложки или иных средств, которые помогут продвинуть проект.
    """

    MIXING = auto()
    MASTERING = auto()
    BEATMAKING = auto()
    PROMOTION = auto()
    RECORDING = auto()
    DESIGNING = auto()
