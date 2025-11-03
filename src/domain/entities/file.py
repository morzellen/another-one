from datetime import datetime
from uuid import UUID

from ..enums import FileFormatEnum, FileTypesEnum


class File:
    """
    Entity. Represents a file that belongs to a project.
    It can be audio, video or image and can be uploaded by employee or client.
    """

    def __init__(
        self,
        id: UUID,
        project_id: UUID,
        subproject_id: UUID | None,
        uploaded_by: UUID,
        uploaded_at: datetime,
        file_type: FileTypesEnum,
        format: FileFormatEnum,
        url: str,
        archived_at: datetime | None = None,
    ):
        self._id = id
        self._project_id = project_id
        self._subproject_id = subproject_id
        self._uploaded_by = uploaded_by
        self._uploaded_at = uploaded_at
        self._file_type = file_type
        self._format = format
        self._url = url
        self._archived_at = archived_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def project_id(self) -> UUID:
        return self._project_id

    @property
    def subproject_id(self) -> UUID | None:
        return self._subproject_id

    @property
    def uploaded_by(self) -> UUID:
        return self._uploaded_by

    @property
    def uploaded_at(self) -> datetime:
        return self._uploaded_at

    @property
    def file_type(self) -> FileTypesEnum:
        return self._file_type

    @property
    def format(self) -> FileFormatEnum:
        return self._format

    @property
    def url(self) -> str:
        return self._url

    @property
    def archived_at(self) -> datetime | None:
        return self._archived_at

    def is_archived(self) -> bool:
        """Checks if the file is archived."""
        return self._archived_at is not None

    def archive(self):
        """Archives the file."""
        if not self.is_archived():
            from datetime import datetime

            self._archived_at = datetime.now()

    def restore(self):
        """Restores the file from archive."""
        self._archived_at = None
