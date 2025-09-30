from enum import Enum


class UserRoleEnum(Enum):
    """
    This class represents the different user roles in the recording studio management platform.
    Each role has specific permissions and capabilities within the system.
    """

    CLIENT: str = "client"
    OWNER: str = "owner"
    ENGINEER: str = "engineer"
    DESIGNER: str = "designer"


class UserStatusesEnum(Enum):
    """
    This class represents the different statuses that a user can have in the system.
    These statuses help track the user's relationship with the studio over time.
    """

    NEW: str = "new"
    ACTIVE: str = "active"
    VIP: str = "vip"
    INACTIVE: str = "inactive"
    BANNED: str = "banned"


class BookingStatusesEnum(Enum):
    """
    This class represents the different statuses that a booking can have throughout its lifecycle.
    These statuses track the progress and state of studio bookings.
    """

    CREATED: str = "created"
    CONFIRMED: str = "confirmed"
    CANCELLED: str = "cancelled"
    COMPLETED: str = "completed"
    RESCHEDULED: str = "rescheduled"


class PaymentStatusesEnum(Enum):
    """
    This class represents the different payment statuses for transactions in the system.
    These statuses indicate whether payments have been processed or are pending.
    """

    PAID: str = "paid"
    UNPAID: str = "unpaid"


class PaymentMethodsEnum(Enum):
    """
    This class represents the different payment methods available for transactions in the system.
    These methods allow clients to pay for studio services using various options.
    """

    CASH: str = "cash"
    CARD: str = "card"


class SubProjectStatusesEnum(Enum):
    """
    This class represents the basic statuses that a subproject can have.
    Subprojects are components of larger projects handled by different team members.
    """

    ASSIGNED = "assigned"
    IN_PROGRESS: str = "in_progress"
    COMPLETED: str = "completed"


class ProjectStatusesEnum(Enum):
    """
    This class represents the statuses that a project can have, extending subproject statuses.
    Projects can be archived when they are completed and no longer active.
    """

    DRAFT: str = "draft"  # client is planning
    ACTIVE: str = "active"  # has active bookings/subprojects
    COMPLETED: str = "completed"  # all is done
    ARCHIVED: str = "archived"  # forgotten


class TaskStatusesEnum(Enum):
    """
    This class represents the different statuses that individual tasks can have.
    Tasks are specific work items within subprojects that need to be completed.
    """

    NEW: str = "new"
    IN_PROGRESS: str = "in_progress"
    COMPLETED: str = "completed"


class FileTypesEnum(Enum):
    """
    This class represents the different categories of file types supported in the system.
    These categories help organize and manage different media files within projects.
    """

    IMAGE: str = "image"
    VIDEO: str = "video"
    AUDIO: str = "audio"


class AudioFormatsEnum(Enum):
    """
    This class represents the supported audio file formats in the system.
    These formats are used for uploading and downloading audio files in projects.
    """

    MP3: str = ".mp3"
    WAV: str = ".wav"


class VideoFormatsEnum(Enum):
    """
    This class represents the supported video file formats in the system.
    These formats are used for uploading and downloading video files in projects.
    """

    MP4: str = ".mp4"
    AVI: str = ".avi"


class ImageFormatsEnum(Enum):
    """
    This class represents the supported image file formats in the system.
    These formats are used for uploading and downloading image files in projects.
    """

    JPEG: str = ".jpeg"
    PNG: str = ".png"


class ServicesTypesEnum(Enum):
    """
    This class represents the different types of services offered by the recording studio.
    These services can be selected by clients when creating bookings and projects.
    """

    MIXING: str = "mixing"
    MASTERING: str = "mastering"
    DISTRIBUTION: str = "distribution"
    BEATMAKING: str = "beatmaking"
    PROMOTION: str = "promotion"
    GHOSTWRITING: str = "ghostwriting"
    RECORDING: str = "recording"


class PricingPlanEnum(Enum):
    """
    This class represents the different pricing plans available in the SaaS platform.
    These plans determine the features and capabilities available to users.
    """

    BASIC: str = "basic"
    PRO: str = "pro"


class CommunicationChannelsTypesEnum(Enum):
    """
    This class represents the different communication channels available for client interaction.
    These channels allow studio staff to communicate with clients through various platforms.
    """

    INSTAGRAM: str = "instagram"
    TELEGRAM: str = "telegram"
    VK: str = "vk"
    WHATSAPP: str = "whatsapp"


class AuthProviderEnum(Enum):
    """
    This class represents the different authentication providers supported by the platform.
    These providers allow users to sign in using their existing social media accounts.
    """

    GOOGLE: str = "google"
    YANDEX: str = "yandex"
    VK: str = "vk"
    TELEGRAM: str = "telegram"
