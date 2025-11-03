from datetime import datetime
from uuid import UUID

from ..enums import TaskStatusesEnum


class Task:
    """
    This class represents the task, wich is part of subproject and the employee
    assigns to himself.
    """

    def __init__(
        self,
        id: UUID,
        subproject_id: UUID,
        title: str,
        created_by: UUID,
        created_at: datetime,
        updated_at: datetime | None = None,
        description: str | None = None,
        status: TaskStatusesEnum = TaskStatusesEnum.NEW,
        completed_at: datetime | None = None,
    ):
        self._id = id
        self._subproject_id = subproject_id
        self._title = self._validate_title(title)
        self._created_by = created_by
        self._created_at = created_at
        self._updated_at = updated_at
        self._description = description
        self._status = status
        self._completed_at = completed_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def subproject_id(self) -> UUID:
        return self._subproject_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def created_by(self) -> UUID:
        return self._created_by

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def status(self) -> TaskStatusesEnum:
        return self._status

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    def _validate_title(self, title: str) -> str:
        """Валидирует заголовок задачи."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        return title.strip()

    def update_title(self, new_title: str):
        """Обновляет заголовок задачи."""
        self._title = self._validate_title(new_title)
        self._updated_at = datetime.now()

    def update_description(self, new_description: str):
        """Обновляет описание задачи."""
        self._description = new_description
        self._updated_at = datetime.now()

    def mark_as_in_progress(self):
        """Отмечает задачу как в работе."""
        if self._status != TaskStatusesEnum.NEW:
            raise ValueError("Cannot start task that is not in NEW status")
        self._status = TaskStatusesEnum.IN_PROGRESS
        self._updated_at = datetime.now()

    def mark_as_completed(self):
        """Отмечает задачу как завершенную."""
        if self._status != TaskStatusesEnum.IN_PROGRESS:
            raise ValueError("Cannot complete task that is not in progress")
        self._status = TaskStatusesEnum.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = datetime.now()

    def is_completed(self) -> bool:
        """Проверяет, завершена ли задача."""
        return self._status == TaskStatusesEnum.COMPLETED
