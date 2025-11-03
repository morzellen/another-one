from datetime import datetime
from uuid import UUID

from ..value_objects.employee_info import EmployeeInfo

from ..enums import UserRoleEnum, UserStatusesEnum


class UserStudioMembership:
    """
    Links a User to a Studio with specific roles and context.
    One User can have multiple memberships (e.g., client in Studio A, engineer in Studio B).
    This is the core of multi-studio isolation.
    """

    def __init__(
        self,
        user_id: UUID,
        studio_id: UUID,
        joined_at: datetime,
        updated_at: datetime | None = None,
        roles: set[UserRoleEnum] | None = None,
        status: UserStatusesEnum = UserStatusesEnum.ACTIVE,
        employee_info: EmployeeInfo | None = None,
        design_style_ids: list[UUID] | None = None,
    ):
        self._user_id = user_id
        self._studio_id = studio_id
        self._joined_at = joined_at
        self._updated_at = updated_at
        self._roles = roles or set()
        self._status = status
        self._employee_info = employee_info
        self._design_style_ids = design_style_ids or []

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def studio_id(self) -> UUID:
        return self._studio_id

    @property
    def joined_at(self) -> datetime:
        return self._joined_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def roles(self) -> set[UserRoleEnum]:
        return self._roles.copy()  # Возвращаем копию для защиты

    @property
    def status(self) -> UserStatusesEnum:
        return self._status

    @property
    def employee_info(self) -> EmployeeInfo | None:
        return self._employee_info

    @property
    def design_style_ids(self) -> list[UUID]:
        return self._design_style_ids.copy()  # Возвращаем копию для защиты

    def is_active(self) -> bool:
        return self._status != UserStatusesEnum.BANNED

    def has_role(self, role: UserRoleEnum) -> bool:
        return role in self._roles

    def is_owner(self) -> bool:
        return UserRoleEnum.OWNER in self._roles

    def is_client_or_employee(self) -> bool:
        return any(
            role
            in [
                UserRoleEnum.CLIENT,
                UserRoleEnum.DESIGNER,
                UserRoleEnum.ENGINEER,
                UserRoleEnum.BEATMAKER,
            ]
            for role in self._roles
        )

    def add_role(self, role: UserRoleEnum):
        if role not in self._roles:
            self._roles.add(role)
            self._updated_at = datetime.now()

    def remove_role(self, role: UserRoleEnum):
        if role in self._roles:
            self._roles.remove(role)
            self._updated_at = datetime.now()

    def get_roles_as_list(self) -> list[str]:
        return [role.value for role in self._roles]

    def update_employee_info(self, new_employee_info: EmployeeInfo):
        """Обновляет информацию о сотруднике."""
        if new_employee_info is not None and not isinstance(new_employee_info, EmployeeInfo):
            raise ValueError("Employee info must be an EmployeeInfo instance or None")
        self._employee_info = new_employee_info
        self._updated_at = datetime.now()

    def ban(self):
        """Блокирует пользователя."""
        self._status = UserStatusesEnum.BANNED
        self._updated_at = datetime.now()

    def unban(self):
        """Разблокирует пользователя."""
        self._status = UserStatusesEnum.ACTIVE
        self._updated_at = datetime.now()

    def add_design_style_id(self, style_id: UUID):
        """Добавляет ID стиля дизайна."""
        if style_id not in self._design_style_ids:
            self._design_style_ids.append(style_id)
            self._updated_at = datetime.now()

    def remove_design_style_id(self, style_id: UUID):
        """Удаляет ID стиля дизайна."""
        if style_id in self._design_style_ids:
            self._design_style_ids.remove(style_id)
            self._updated_at = datetime.now()
