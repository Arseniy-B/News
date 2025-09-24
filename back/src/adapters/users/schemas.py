from pydantic import BaseModel
from src.domain.port.users import (
    UserLogin as ABCUserLogin,
    UserCreate as ABCUserCreate,
)
from enum import Enum
from datetime import datetime
from src.domain.port.users import UserAuthId as ABCUserAuthId


class UserLogin(ABCUserLogin):
    pass

class UserCreate(ABCUserCreate):
    pass


class UserAuthId(BaseModel, ABCUserAuthId):
    access_token: str
    refresh_token: str


class JWTType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTPayload(BaseModel):
    exp: datetime = datetime.today()
    iat: datetime = datetime.today()
    sub: str 
    token_type: JWTType
    username: str

