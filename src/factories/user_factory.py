from uuid import UUID
from datetime import datetime

from ..entities.user import User
from ..value_objects.value_objects import ContactInfo, Email, PersonalInfo


class UserFactory:
    @staticmethod
    def create_user(email: str, first_name: str = None, last_name: str = None) -> User:
        contact_info = ContactInfo(email=Email(email))
        personal_info = PersonalInfo(first_name=first_name, last_name=last_name)
        return User(
            id=UUID(...),
            contact_info=contact_info,
            personal_info=personal_info,
            created_at=datetime.now(),
        )
