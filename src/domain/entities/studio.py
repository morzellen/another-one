from datetime import datetime
from uuid import UUID
from ..value_objects.studio_configuration import StudioConfiguration
from ..errors import InvalidStudioConfigurationError


class Studio:
    """
    Сущность, представляющая студию звукозаписи на платформе управления студиями.
    Студии являются центральными местами, где клиенти могут создавать проекты,
    покупать услуги и т.д. Студиями управляют владельцы и они имеют
    уникальный идентификатор (UUID). Это основная часть SaaS-системы,
    где происходит вся активность. Сначала создается студия (по желанию
    с новой пробной подпиской), а затем к ней можно привязывать
    и обновлять подписки. На студиях завязаны работники, клиенты —
    в общем, пользователи. У 1 студии может быть только 1 владелец.
    У 1 владельца может быть несколько студий.
    Поля:
        id (UUID):
            Уникальный идентификатор студии.
        owner_id (UUID):
            Идентификатор пользователя, являющегося владельцем студии.
        name (str):
            Название студии.
        created_at (datetime):
            Дата и время создания студии.
        updated_at (datetime | None):
            Дата и время последнего обновления студии (опционально).
        subscription_id (UUID | None):
            Идентификатор активной подписки, связанной со студией (опционально).
        configuration (StudioConfiguration | None):
            Конфигурация студии, содержащая описание, логотип и политику скидок (опционально).
    """

    def __init__(
        self,
        id: UUID,
        owner_id: UUID,
        name: str,
        created_at: datetime,
        updated_at: datetime | None = None,
        subscription_id: UUID | None = None,
        configuration: StudioConfiguration | None = None,
    ):
        self._id = id
        self._owner_id = owner_id
        self._name = self._validate_name(name)
        self._created_at = created_at
        self._updated_at = updated_at
        self._subscription_id = subscription_id
        self._configuration = configuration

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def owner_id(self) -> UUID:
        return self._owner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @property
    def subscription_id(self) -> UUID | None:
        return self._subscription_id

    @property
    def configuration(self) -> StudioConfiguration | None:
        return self._configuration

    def _validate_name(self, name: str) -> str:
        """Валидирует название студии."""
        if not name or not name.strip():
            raise ValueError("Studio name cannot be empty")
        return name.strip()

    def has_subscription(self) -> bool:
        return self._subscription_id is not None

    def rename(self, new_name: str):
        """
        Изменяет название студии.
        """
        self._name = self._validate_name(new_name)
        self._updated_at = datetime.now()

    def update_configuration(self, new_configuration: StudioConfiguration):
        """
        Обновляет конфигурацию студии.
        """
        if new_configuration is not None and not isinstance(new_configuration, StudioConfiguration):
            raise InvalidStudioConfigurationError(
                "Configuration must be a StudioConfiguration instance"
            )
        self._configuration = new_configuration
        self._updated_at = datetime.now()

    def assign_subscription(self, subscription_id: UUID):
        """Привязывает подписку к студии."""
        self._subscription_id = subscription_id
        self._updated_at = datetime.now()

    def remove_subscription(self):
        """Отвязывает подписку от студии."""
        self._subscription_id = None
        self._updated_at = datetime.now()
