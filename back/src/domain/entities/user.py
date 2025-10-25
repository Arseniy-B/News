import re
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


@dataclass
class UserCreate:
    username: str
    password: str
    email: str
    password: str

    def __post_init__(self):
        if not isinstance(self.username, str):
            raise ValidationError("username", "not string")
        if not isinstance(self.password, str):
            raise ValidationError("password", "not string")
        if not isinstance(self.email, str):
            raise ValidationError("email", "not string")

        if not bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email)):
            raise ValidationError("email", "wrong email adress")
        if len(self.password) < 5:
            raise ValidationError("password", "the password is not strong enough")
        if len(self.password) > 100:
            raise ValidationError("password", "password too long")
        if len(self.username) < 2:
            raise ValidationError("username", "username too smoll")
        if len(self.username) > 25:
            raise ValidationError("username", "username too long")


@dataclass
class UserLogin:
    password: str
    username: str | None = None
    email: str | None = None

    def __post_init__(self):
        if not isinstance(self.username, str) and not self.username:
            raise ValidationError("username", "not string")
        if not isinstance(self.password, str):
            raise ValidationError("password", "not string")
        if not isinstance(self.email, str) and not self.username:
            raise ValidationError("email", "not string")

        if not self.username and not self.email:
            raise ValidationError(
                "username email", "at least one of the fields must be present"
            )
        if self.email:
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", self.email):
                raise ValidationError("email", "wrong email adress")
        if not len(self.password) > 5:
            raise ValidationError("password", "the password is not strong enough")
        if not len(self.password) < 100:
            raise ValidationError("password", "password too long")
        if self.username:
            if len(self.username) < 2:
                raise ValidationError("username", "username too smoll")
            if len(self.username) > 25:
                raise ValidationError("username", "username too long")
