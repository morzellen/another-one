import hashlib
import secrets


class PasswordHasher:
    """
    Сервис класс для хэширования и верификации паролей.
    Использует PBKDF2-HMAC-SHA256 с солью.
    Не является dataclass, так как содержит поведение.
    """

    @staticmethod
    def hash(password: str) -> str:
        """Хэширует пароль и возвращает строку в формате 'salt$hash'."""
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
        )
        pwdhash_hex = pwdhash.hex()
        return f"{salt}${pwdhash_hex}"

    @staticmethod
    def verify(stored_hash: str, password: str) -> bool:
        """Проверяет, соответствует ли пароль сохранённому хэшу."""
        if not isinstance(stored_hash, str) or not isinstance(password, str):
            return False
        try:
            salt, stored_pwdhash = stored_hash.split("$")
            pwdhash = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
            )
            return pwdhash.hex() == stored_pwdhash
        except (ValueError, TypeError):
            return False
