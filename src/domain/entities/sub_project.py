from datetime import datetime
from uuid import UUID

from ..enums import ServicesTypesEnum, SubProjectStatusesEnum


class SubProject:
    """
    Aggregate root for tasks and files.
    """

    def __init__(
        self,
        id: UUID,
        project_id: UUID,
        created_by: UUID,  # who created subproject and working with it (only emplyoee can do that)
        updated_at: datetime,
        service_type: ServicesTypesEnum,
        booking_id: UUID | None = None,
        status: SubProjectStatusesEnum = SubProjectStatusesEnum.ASSIGNED,
        tasks_ids: list[UUID] | None = None,
        files_ids: list[UUID] | None = None,
        completed_at: datetime | None = None,
    ):
        self._id = id
        self._project_id = project_id
        self._created_by = created_by
        self._updated_at = updated_at
        self._service_type = service_type
        self._booking_id = booking_id
        self._status = status
        self._tasks_ids = tasks_ids or []
        self._files_ids = files_ids or []
        self._completed_at = completed_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def project_id(self) -> UUID:
        return self._project_id

    @property
    def created_by(self) -> UUID:
        return self._created_by

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def service_type(self) -> ServicesTypesEnum:
        return self._service_type

    @property
    def booking_id(self) -> UUID | None:
        return self._booking_id

    @property
    def status(self) -> SubProjectStatusesEnum:
        return self._status

    @property
    def tasks_ids(self) -> list[UUID]:
        return self._tasks_ids.copy()

    @property
    def files_ids(self) -> list[UUID]:
        return self._files_ids.copy()

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    def add_task(self, task_id: UUID):
        """Adds a task to the subproject."""
        if task_id not in self._tasks_ids:
            self._tasks_ids.append(task_id)
            self._updated_at = datetime.now()

    def remove_task(self, task_id: UUID):
        """Removes a task from the subproject."""
        if task_id in self._tasks_ids:
            self._tasks_ids.remove(task_id)
            self._updated_at = datetime.now()

    def add_file(self, file_id: UUID):
        """Adds a file to the subproject."""
        if file_id not in self._files_ids:
            self._files_ids.append(file_id)
            self._updated_at = datetime.now()

    def remove_file(self, file_id: UUID):
        """Removes a file from the subproject."""
        if file_id in self._files_ids:
            self._files_ids.remove(file_id)
            self._updated_at = datetime.now()

    def mark_as_in_progress(self):
        """Marks the subproject as in progress."""
        if self._status != SubProjectStatusesEnum.ASSIGNED:
            raise ValueError("Cannot start subproject that is not assigned")
        self._status = SubProjectStatusesEnum.IN_PROGRESS
        self._updated_at = datetime.now()

    def mark_as_completed(self):
        """Marks the subproject as completed."""
        if self._status != SubProjectStatusesEnum.IN_PROGRESS:
            raise ValueError("Cannot complete subproject that is not in progress")
        self._status = SubProjectStatusesEnum.COMPLETED
        self._completed_at = datetime.now()
        self._updated_at = datetime.now()

    def is_completed(self) -> bool:
        """Checks if the subproject is completed."""
        return self._status == SubProjectStatusesEnum.COMPLETED
