from src.domain.utils.otp import Otp
from pydantic import BaseModel, EmailStr, field_validator

from src.domain.entities.user import (
    UserCreate as ABCUserCreate,
)
from src.domain.entities.user import (
    UserLogin as ABCUserLogin,
)
from src.domain.exceptions import ValidationError


class UserLogin(BaseModel, ABCUserLogin):
    email: EmailStr
    code: Otp

    @field_validator("email")
    @classmethod
    def validate_email(cls, v, info):
        if not v and not info.data.get("username"):
            raise ValidationError(
                "username/email", "at least one of the fields must be present"
            )
        return v
