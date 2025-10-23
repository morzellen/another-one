from uuid import UUID
from datetime import datetime

from ..entities.user import User
from ..repositories.session_repository import SessionRepository


class SessionService:
    def __init__(self, session_repo: SessionRepository):
        self.session_repo = session_repo

    def create_session(self, user: User) -> str:
        """Создаёт сессию для пользователя."""
        session_id = str(UUID(...))  # Генерация ID
        self.session_repo.save(session_id, user.id, datetime.now())
        return session_id

    def logout(self, session_id: str):
        """Завершает сессию."""
        self.session_repo.delete(session_id)
