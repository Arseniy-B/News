from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from src.domain.entities.user import (
    UserCreate as ABCUserCreate,
)
from src.domain.entities.user import (
    UserLogin as ABCUserLogin,
)
from src.domain.exceptions import ValidationError


class UserJWT(BaseModel):
    access_token: str
    refresh_token: str | None


class JWTType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTPayload(BaseModel):
    exp: datetime = datetime.today()
    iat: datetime = datetime.today()
    sub: str
    token_type: JWTType
    username: str



class UserLogin(BaseModel, ABCUserLogin):
    password: str
    username: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 5:
            raise ValidationError("password", "the password is not strong enough")
        if len(v) > 100:
            raise ValidationError("password", "password too long")
        return v

    @field_validator("username")
    @classmethod
    def validate_username(cls, v, info):
        if len(v) < 2:
            raise ValidationError("username", "username too small")
        if len(v) > 25:
            raise ValidationError("username", "username too long")
        return v
