from enum import StrEnum


class UserRoleEnum(StrEnum):
    """
    This class represents the different user roles in the recording studio management platform.
    Each role has specific permissions and capabilities within the system.
    """

    POTENTIAL_BUYER: str = "potential_buyer"
    CLIENT: str = "client"
    OWNER: str = "owner"
    ENGINEER: str = "engineer"
    DESIGNER: str = "designer"
    BEATMAKER: str = "beatmaker"
    GHOSTWRITER: str = "ghostwriter"


class UserStatusesEnum(StrEnum):
    """
    This class represents the different statuses that a user can have in the system.
    These statuses help track the user's relationship with the studio over time.

    The fields in this class are:
    - NEW: The user has just created their account and is awaiting confirmation.
    - ACTIVE: The user is active and has access to the platform's features.
    - VIP: The user has been designated VIP status and has access to premium features.
    - BANNED: The user has been banned and no longer has access to the platform's features.
    """

    NEW: str = "new"
    ACTIVE: str = "active"
    VIP: str = "vip"
    BANNED: str = "banned"


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

    CREATED: str = "created"
    CONFIRMED: str = "confirmed"
    CANCELLED: str = "cancelled"
    COMPLETED: str = "completed"
    RESCHEDULED: str = "rescheduled"


class SubProjectStatusesEnum(StrEnum):
    """
    This class represents the basic statuses that a subproject can have.
    Subprojects are components of larger projects handled by different team members.
    """

    ASSIGNED: str = "assigned"
    IN_PROGRESS: str = "in_progress"
    COMPLETED: str = "completed"


class ProjectStatusesEnum(StrEnum):
    """
    This class represents the statuses that a project can have, extending subproject statuses.
    Projects can be archived when they are completed and no longer active.
    """

    DRAFT: str = "draft"  # client is planning
    ACTIVE: str = "active"  # has active bookings/subprojects
    COMPLETED: str = "completed"  # all is done
    ARCHIVED: str = "archived"  # forgotten


class TaskStatusesEnum(StrEnum):
    """
    This class represents the different statuses that individual tasks can have.
    Tasks are specific work items within subprojects that need to be completed.
    """

    NEW: str = "new"
    IN_PROGRESS: str = "in_progress"
    COMPLETED: str = "completed"


class FileTypesEnum(StrEnum):
    """
    This class represents the different categories of file types supported in the system.
    These categories help organize and manage different media files within projects.
    """

    IMAGE: str = "image"
    VIDEO: str = "video"
    AUDIO: str = "audio"


class FileFormatEnum(StrEnum):
    """
    This class represents the supported file formats in the system.
    These formats are used for uploading and downloading files in projects.
    """

    MP3: str = ".mp3"
    WAV: str = ".wav"
    MP4: str = ".mp4"
    AVI: str = ".avi"
    JPEG: str = ".jpeg"
    PNG: str = ".png"


class ServicesTypesEnum(StrEnum):
    """
    This class represents the different types of services offered by the recording studio.
    These services can be selected by clients when creating projects.
    """

    MIXING: str = "mixing"
    MASTERING: str = "mastering"
    DISTRIBUTION: str = "distribution"
    BEATMAKING: str = "beatmaking"
    PROMOTION: str = "promotion"
    GHOSTWRITING: str = "ghostwriting"
    RECORDING: str = "recording"
    DESIGNING: str = "designing"


class PricingPlanEnum(StrEnum):
    """
    This class represents the different pricing plans available in the SaaS platform.
    These plans determine the features and capabilities available to users.

    The fields in this class are:
    - LIFETIME: A lifetime tariff plan that offers unlimited access to the platform's features.
    - TRIAL: A trial tariff plan that is free and time-limited. In terms of functionality: BASIC.
    - BASIC: The basic pricing plan, which offers limited features and capabilities.
    - PRO: The pro pricing plan, which offers full features and capabilities.
    """

    LIFETIME = "lifetime"
    TRIAL: str = "trial"
    BASIC: str = "basic"
    PRO: str = "pro"


class CommunicationChannelsTypesEnum(StrEnum):
    """
    This class represents the different communication channels available for client interaction.
    These channels allow studio staff to communicate with clients through various platforms.
    """

    INSTAGRAM: str = "instagram"
    TELEGRAM: str = "telegram"
    VK: str = "vk"
    WHATSAPP: str = "whatsapp"


class AuthProviderEnum(StrEnum):
    """
    This class represents the different authentication providers supported by the platform.
    These providers allow users to sign in using their existing social media accounts.
    """

    NATIVE: str = "native"
    GOOGLE: str = "google"
    YANDEX: str = "yandex"
    VK: str = "vk"
    TELEGRAM: str = "telegram"


class SubscriptionStatusesEnum(StrEnum):
    """
    This class represents the different statuses that a user's subscription can have.

    The fields in this class are:
    - ACTIVE: The subscription is currently active and the user has access to the platform's features.
    - PENDING: The subscription has been created but payment is still pending.
    - EXPIRED: The subscription has expired and the user no longer has access to the platform's features.
    - CANCELLED: The subscription has been cancelled and the user no longer has access to the platform's features.
    """

    ACTIVE: str = "active"
    PENDING: str = "pending"
    EXPIRED: str = "expired"
    CANCELLED: str = "cancelled"
