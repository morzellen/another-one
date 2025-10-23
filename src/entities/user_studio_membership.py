from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .studio import Studio
from ..constants import ROLE_FUNCTIONALITY
from ..enums import UserRoleEnum, UserStatusesEnum
from ..value_objects.value_objects import EmployeeInfo


@dataclass
class UserStudioMembership:
    """
    Links a User to a Studio with specific roles and context.
    One User can have multiple memberships (e.g., client in Studio A, engineer in Studio B).
    This is the core of multi-studio isolation.
    """

    user_id: UUID
    studio_id: UUID
    roles: set[UserRoleEnum] = field(default_factory=set)
    status: UserStatusesEnum = UserStatusesEnum.ACTIVE

    joined_at: datetime
    updated_at: datetime | None = None

    # Studio-specific extensions (only populated if relevant roles are present)
    employee_info: EmployeeInfo | None = None  # for ENGINEER, DESIGNER, etc.
    # Note: discount eligibility, pricing overrides, etc. can go here later
    design_style_ids: list[UUID] | None = field(default_factory=list)

    def is_active(self) -> bool:
        return self.status != UserStatusesEnum.BANNED

    def has_role(self, role: UserRoleEnum) -> bool:
        return role in self.roles

    def is_owner(self) -> bool:
        return UserRoleEnum.OWNER in self.roles

    def is_client_or_employee(self) -> bool:
        return any(
            r in [UserRoleEnum.CLIENT, UserRoleEnum.DESIGNER, UserRoleEnum.ENGINEER]
            for r in self.roles
        )

    def add_role(self, role: UserRoleEnum):
        if role not in self.roles:
            self.roles.add(role)
            self.updated_at = datetime.now()

    def remove_role(self, role: UserRoleEnum):
        if role in self.roles:
            self.roles.remove(role)
            self.updated_at = datetime.now()

    def get_roles_as_list(self) -> list[str]:
        return [role.value for role in self.roles]
