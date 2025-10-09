import jwt
from src.config import config
from datetime import timedelta, datetime, timezone
from src.infrastructure.adapters.auth.schemas import UserJWT, JWTPayload, JWTType
from src.domain.entities.user import User


def encode_jwt(
    payload: JWTPayload,
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm=config.auth_jwt.algorithm,
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
    algorithm: str = config.auth_jwt.algorithm,
) -> JWTPayload:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return JWTPayload(**decoded)


def create_jwt(
    token_type: JWTType,
    user: User,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
) -> str:
    jwt_payload = JWTPayload(
        sub=str(user.id), username=user.username, token_type=token_type
    )
    return encode_jwt(jwt_payload, expire_minutes=expire_minutes)


def create_access_token(user: User) -> str:
    return create_jwt(JWTType.ACCESS, user)


def create_refresh_token(user: User) -> str:
    return create_jwt(
        JWTType.REFRESH,
        user,
        expire_minutes=config.auth_jwt.refresh_token_expire_minutes,
    )

def refresh_token_info(payload: JWTPayload):
    return UserJWT(
        access_token=encode_jwt(
            payload, expire_minutes=config.auth_jwt.access_token_expire_minutes
        ),
        refresh_token=encode_jwt(
            payload, expire_minutes=config.auth_jwt.refresh_token_expire_minutes
        )
    )

def create_token_info(user: User) -> UserJWT:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return UserJWT(access_token=access_token, refresh_token=refresh_token)
