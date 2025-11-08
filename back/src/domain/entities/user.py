import re
from abc import ABC
from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import ValidationError


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    email: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not all([
            self.id >= 0,
            2 <= len(self.username) <= 25,
            re.match(
                r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email
            ),
            self.created_at < self.updated_at,
        ]):
            raise ValidationError()


@dataclass
class UserCreate(ABC):
    pass


@dataclass
class UserLogin(ABC):
    pass
