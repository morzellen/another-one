from datetime import datetime
from uuid import UUID


class DesignStyle:
    """
    Entity. Represents a design style, which is part of designer profile.
    It can be a name of style like minimalistic, modern, etc.
    """

    def __init__(self, id: UUID, studio_id: UUID, name: str, created_at: datetime):
        self._id = id
        self._studio_id = studio_id
        self._name = self._validate_name(name)
        self._created_at = created_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def studio_id(self) -> UUID:
        return self._studio_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def _validate_name(self, name: str) -> str:
        """Validates the design style name."""
        if not name or not name.strip():
            raise ValueError("Design style name cannot be empty")
        return name.strip()

    def rename(self, new_name: str):
        """Renames the design style."""
        self._name = self._validate_name(new_name)
