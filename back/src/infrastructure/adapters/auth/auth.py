import jwt
from fastapi import Request, Response

from src.config import config
from src.domain.entities.user import User
from src.domain.port.users import AuthPort
from src.infrastructure.adapters.auth.schemas import UserJWT
from src.infrastructure.adapters.auth.utils.jwt import (
    create_token_info,
    decode_jwt,
    refresh_token_info,
)
from src.infrastructure.exceptions import AuthRepoError, TokenError
from src.infrastructure.services.redis.redis import redis_helper


class AuthAdapter(AuthPort):
    def __init__(self, request: Request, response: Response):
        self._request = request
        self._response = response
        self._user_jwt = self.get_user_jwt()

    def set_user_jwt(self, user_jwt: UserJWT):
        if not user_jwt.refresh_token:
            raise TokenError
        conf = {
            "httponly": True,
            "secure": True,
            "samesite": "none",
            "max_age": config.auth_jwt.refresh_token_expire_minutes,
            "path": "/",
        }
        self._response.set_cookie(
            key="refresh_token", value=user_jwt.refresh_token, **conf
        )
        self._response.headers["Authorization"] = f"Bearer {user_jwt.access_token}"

    def get_user_jwt(self) -> UserJWT | None:
        refresh_token, access_token = None, None

        if "Authorization" in self._request.headers:
            access_token = self._request.headers["Authorization"]
            access_token = access_token.split()
            if access_token[0] != "Bearer":
                raise TokenError
            access_token = access_token[1]

        if "refresh_token" in self._request.cookies:
            refresh_token = self._request.cookies.get("refresh_token")

        if access_token:
            user_jwt = UserJWT(access_token=access_token, refresh_token=refresh_token)
            return user_jwt
        return None

    def refresh_token(self):
        if not self._user_jwt or not self._user_jwt.refresh_token:
            raise TokenError
        try:
            payload = decode_jwt(self._user_jwt.refresh_token)
        except jwt.PyJWTError:
            raise TokenError
        self.set_user_jwt(refresh_token_info(payload))

    def login(self, user: User):
        user_jwt = create_token_info(user)
        self._user_jwt = user_jwt
        self.set_user_jwt(user_jwt)

    async def logout(self):
        redis = await redis_helper.get_redis()
        if not self._user_jwt or not self._user_jwt.refresh_token:
            raise TokenError
        await redis.set(self._user_jwt.refresh_token, "True")
        await redis.set(self._user_jwt.access_token, "True")

    async def is_authenticated(self) -> bool:
        if not self._user_jwt or not self._user_jwt.refresh_token:
            return False

        redis = await redis_helper.get_redis()
        if await redis.get(self._user_jwt.refresh_token) or await redis.get(
            self._user_jwt.access_token
        ):
            return False

        try:
            decode_jwt(self._user_jwt.access_token)
            return True
        except jwt.PyJWTError:
            raise TokenError

    def get_user_id(self) -> int | None:
        if not self._user_jwt:
            return None
        try:
            payload = decode_jwt(self._user_jwt.access_token)
        except jwt.PyJWTError:
            return None
        return int(payload.sub)
