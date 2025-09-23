from pydantic import BaseModel
from src.domain.port.users import (
    UserLogin as ABCUserLogin,
    UserCreate as ABCUserCreate,
)


class UserLogin(ABCUserLogin):
    username: str
    password: str


class UserCreate(ABCUserCreate):
    username: str
    password1: str
    password2: str

