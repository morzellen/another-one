from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserAudit:
    id: UUID
    studio_id: UUID
    user_id: UUID
    field_name: str  # for example: "contact_info.email"
    new_value: str  # serialized value
    changed_by: UUID  # who changed
    changed_at: datetime
    old_value: str | None = None  # serialized value (str or None)


@dataclass
class BookingAudit:
    id: UUID
    studio_id: UUID
    booking_id: UUID
    field_name: str  # for example: "time_range.start_time", "status", "payment_status"
    new_value: str  # serialized value
    updated_by: UUID  # who updated
    updated_at: datetime
    old_value: str | None = None  # serialized value (str or None)
