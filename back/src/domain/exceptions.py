from abc import ABC
from typing import Any, Optional


class DomainError(Exception, ABC):
    """Base domain exception"""


class ValidationError(DomainError):
    """Base domain validation exception"""

    def __init__(self, field: str, value: Optional[Any] = None):
        self.field = field
        self.value = value

        msg = f"Invalid {field}"
        if value is not None:
            msg += f": {value}"
        super().__init__(msg)

    def __str__(self):
        return f"{self.field}: {self.value}"
