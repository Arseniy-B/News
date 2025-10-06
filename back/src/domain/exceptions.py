from abc import ABC
from typing import Any, Optional


class DomainError(Exception, ABC):
    """Base domain exception"""


class UserNotFound(DomainError):
    def __init__(self, user_id: int | None = None):
        super().__init__(f"User {user_id} not found")


class ValidationError(DomainError):
    """Base domain validation exception"""

    def __init__(self, field: str, value: Optional[Any] = None):
        msg = f"Invalid {field}"
        if value is not None:
            msg += f": {value}"
        super().__init__(msg)


class UserRepoError(Exception):
    """Base user repository exception"""


class NewsRepoError(Exception):
    """Base news repository exception"""
