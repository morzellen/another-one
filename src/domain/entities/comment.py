from datetime import datetime
from uuid import UUID


class Comment:
    """
    Entity. Represents a comment on a project. Can be left by owner or client.
    We can consider this a note that a client or studio owner creates, and those
    who work on the project will see it.
    """

    def __init__(
        self,
        id: UUID,
        project_id: UUID,
        left_by: UUID,  # it can be owner or client
        text: str,
        created_at: datetime,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
    ):
        self._id = id
        self._project_id = project_id
        self._left_by = left_by
        self._text = self._validate_text(text)
        self._created_at = created_at
        self._updated_at = updated_at
        self._deleted_at = deleted_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def project_id(self) -> UUID:
        return self._project_id

    @property
    def left_by(self) -> UUID:
        return self._left_by

    @property
    def text(self) -> str:
        return self._text

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def deleted_at(self) -> datetime | None:
        return self._deleted_at

    def _validate_text(self, text: str) -> str:
        """Validates the comment text."""
        if not text or not text.strip():
            raise ValueError("Comment text cannot be empty")
        return text.strip()

    def update_text(self, new_text: str):
        """Updates the comment text."""
        self._text = self._validate_text(new_text)
        self._updated_at = datetime.now()

    def delete(self):
        """Deletes the comment."""
        if self._deleted_at is None:
            from datetime import datetime

            self._deleted_at = datetime.now()
            self._updated_at = datetime.now()

    def is_deleted(self) -> bool:
        """Checks if the comment is deleted."""
        return self._deleted_at is not None

    def restore(self):
        """Restores the comment."""
        self._deleted_at = None
        self._updated_at = datetime.now()
