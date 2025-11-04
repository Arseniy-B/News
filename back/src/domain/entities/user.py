from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    email: str
    created_at: datetime
    updated_at: datetime


@dataclass
class UserCreate(ABC):
    pass


@dataclass
class UserLogin(ABC):
    pass
