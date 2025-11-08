from src.domain.utils.otp import Otp
from pydantic import BaseModel, EmailStr, field_validator

from src.domain.entities.user import (
    UserCreate as ABCUserCreate,
)
from src.domain.entities.user import (
    UserLogin as ABCUserLogin,
)

class UserLogin(BaseModel, ABCUserLogin):
    email: EmailStr
    code: Otp
