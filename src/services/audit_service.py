from datetime import datetime
from uuid import UUID

from ..entities.audits_entities import UserAudit, BookingAudit
from ..repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, audit_repo: AuditRepository):
        self.audit_repo = audit_repo

    def log_user_change(
        self,
        user_id: UUID,
        studio_id: UUID,
        field_name: str,
        old_value: str,
        new_value: str,
        changed_by: UUID,
    ):
        audit = UserAudit(
            id=UUID(...),
            studio_id=studio_id,
            user_id=user_id,
            field_name=field_name,
            new_value=new_value,
            changed_by=changed_by,
            changed_at=datetime.now(),
            old_value=old_value,
        )
        self.audit_repo.save(audit)

    def log_booking_change(
        self,
        booking_id: UUID,
        studio_id: UUID,
        field_name: str,
        old_value: str,
        new_value: str,
        updated_by: UUID,
    ):
        audit = BookingAudit(
            id=UUID(...),
            studio_id=studio_id,
            booking_id=booking_id,
            field_name=field_name,
            new_value=new_value,
            updated_by=updated_by,
            updated_at=datetime.now(),
            old_value=old_value,
        )
        self.audit_repo.save(audit)
