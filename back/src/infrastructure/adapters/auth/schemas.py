from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class UserJWT(BaseModel):
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
