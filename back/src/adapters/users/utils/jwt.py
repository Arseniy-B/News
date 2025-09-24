import jwt
from src.config import config 
from datetime import timedelta, datetime, timezone
from src.adapters.users.schemas import *
from src.adapters.users.users import UserAuthId
from src.domain.entities.user import User


def encode_jwt(
    payload: JWTPayload, 
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm = config.auth_jwt.algorithm,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.model_copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.exp = expire
    to_encode.iat = now

    encoded = jwt.encode(to_encode.model_dump(), private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = config.auth_jwt.public_key_path.read_text(), 
    algorithm: str = config.auth_jwt.algorithm
) -> JWTPayload:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return JWTPayload(**decoded)


async def create_jwt(
    token_type: JWTType, 
    user: User,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
) -> str:
    jwt_payload = JWTPayload(
        sub=str(user.id),
        username=user.username,
        token_type=token_type
    )
    return encode_jwt(jwt_payload, expire_minutes=expire_minutes)


async def create_access_token(user: User) -> str:
    return await create_jwt(JWTType.ACCESS, user)


async def create_refresh_token(user: User) -> str:
    return await create_jwt(
        JWTType.REFRESH, 
        user,  
        expire_minutes=config.auth_jwt.refresh_token_expire_minutes
    )

async def create_token_info(user: User) -> UserAuthId:
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    return UserAuthId(
        access_token=access_token,
        refresh_token=refresh_token
    )

