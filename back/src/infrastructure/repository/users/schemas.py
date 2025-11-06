from pydantic import BaseModel, EmailStr, field_validator
from src.domain.entities.user import (
    UserCreate as ABCUserCreate,
)
from src.domain.exceptions import ValidationError


class UserCreate(BaseModel, ABCUserCreate):
    username: str
    password: str
    email: EmailStr

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 2:
            raise ValidationError("username", "username too small")
        if len(v) > 25:
            raise ValidationError("username", "username too long")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 5:
            raise ValidationError("password", "the password is not strong enough")
        if len(v) > 100:
            raise ValidationError("password", "password too long")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not isinstance(v, str) or not v:
            raise ValidationError("email", "email must be a valid string")
        return v


