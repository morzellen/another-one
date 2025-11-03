from datetime import datetime
from uuid import UUID

from ..enums import ProjectStatusesEnum


class Project:
    """
    This class represents the agregated root of subprojects.
    The project is a kind of work space with studio services, in which the client
    monitors the changes made by the employees.
    He can also create this project for the future, or book time for an existing one.
    Also project can be archived when it is completed and no longer active.
    Project can be created by client or studio owner.
    """

    def __init__(
        self,
        id: UUID,
        studio_id: UUID,
        client_id: UUID,
        created_by: UUID,
        created_at: datetime,
        updated_at: datetime | None = None,
        status: ProjectStatusesEnum = ProjectStatusesEnum.DRAFT,
        subprojects_ids: list[UUID] | None = None,
        comments_ids: list[UUID] | None = None,
        files_ids: list[UUID] | None = None,
        completed_at: datetime | None = None,
        archived_at: datetime | None = None,
    ):
        self._id = id
        self._studio_id = studio_id
        self._client_id = client_id
        self._created_by = created_by
        self._created_at = created_at
        self._updated_at = updated_at
        self._status = status
        self._subprojects_ids = subprojects_ids or []
        self._comments_ids = comments_ids or []
        self._files_ids = files_ids or []
        self._completed_at = completed_at
        self._archived_at = archived_at

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
    def created_by(self) -> UUID:
        return self._created_by

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def status(self) -> ProjectStatusesEnum:
        return self._status

    @property
    def subprojects_ids(self) -> list[UUID]:
        return self._subprojects_ids.copy()

    @property
    def comments_ids(self) -> list[UUID]:
        return self._comments_ids.copy()

    @property
    def files_ids(self) -> list[UUID]:
        return self._files_ids.copy()

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    @property
    def archived_at(self) -> datetime | None:
        return self._archived_at

    def add_subproject(self, subproject_id: UUID):
        """Добавляет подпроект в проект."""
        if subproject_id not in self._subprojects_ids:
            self._subprojects_ids.append(subproject_id)
            self._updated_at = datetime.now()

    def remove_subproject(self, subproject_id: UUID):
        """Удаляет подпроект из проекта."""
        if subproject_id in self._subprojects_ids:
            self._subprojects_ids.remove(subproject_id)
            self._updated_at = datetime.now()

    def add_comment(self, comment_id: UUID):
        """Добавляет комментарий в проект."""
        if comment_id not in self._comments_ids:
            self._comments_ids.append(comment_id)
            self._updated_at = datetime.now()

    def remove_comment(self, comment_id: UUID):
        """Удаляет комментарий из проекта."""
        if comment_id in self._comments_ids:
            self._comments_ids.remove(comment_id)
            self._updated_at = datetime.now()

    def add_file(self, file_id: UUID):
        """Добавляет файл в проект."""
        if file_id not in self._files_ids:
            self._files_ids.append(file_id)
            self._updated_at = datetime.now()

    def remove_file(self, file_id: UUID):
        """Удаляет файл из проекта."""
        if file_id in self._files_ids:
            self._files_ids.remove(file_id)
            self._updated_at = datetime.now()

    def mark_as_active(self):
        """Отмечает проект как активный."""
        if self._status != ProjectStatusesEnum.DRAFT:
            raise ValueError("Cannot activate project that is not in draft status")
        self._status = ProjectStatusesEnum.ACTIVE
        self._updated_at = datetime.now()

    def mark_as_completed(self):
        """Отмечает проект как завершенный."""
        if self._status != ProjectStatusesEnum.ACTIVE:
            raise ValueError("Cannot complete project that is not active")
        self._status = ProjectStatusesEnum.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = datetime.now()

    def archive(self):
        """Архивирует проект."""
        if self._status != ProjectStatusesEnum.COMPLETED:
            raise ValueError("Cannot archive project that is not completed")
        self._status = ProjectStatusesEnum.ARCHIVED
        self._archived_at = datetime.now()
        self._updated_at = datetime.now()

    def is_completed(self) -> bool:
        """Проверяет, завершен ли проект."""
        return self._status == ProjectStatusesEnum.COMPLETED

    def is_archived(self) -> bool:
        """Проверяет, заархивирован ли проект."""
        return self._status == ProjectStatusesEnum.ARCHIVED
