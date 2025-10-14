from fastapi import Request, Response

from src.config import config
from src.domain.entities.user import User
from src.domain.port.users import AuthRepository
from src.infrastructure.adapters.auth.schemas import UserJWT
from src.infrastructure.adapters.auth.utils.jwt import (
    create_token_info,
    decode_jwt,
    refresh_token_info,
)


class AuthAdapter(AuthRepository):
    def __init__(self, request: Request, response: Response):
        self._request = request
        self._response = response
        self._user_jwt = self.get_user_jwt()

    def set_user_jwt(self, user_jwt: UserJWT):
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
                raise
            access_token = access_token[1]

        if "refresh_token" in self._request.cookies:
            refresh_token = self._request.cookies.get("refresh_token")

        if refresh_token and not access_token:
            new_user_jwt = self.refresh_token(refresh_token)
            self.set_user_jwt(new_user_jwt)
            return new_user_jwt

        if refresh_token and access_token:
            user_jwt = UserJWT(access_token=access_token, refresh_token=refresh_token)
            return user_jwt
        return None

    def refresh_token(self, refresh_token: str):
        payload = decode_jwt(refresh_token)
        return refresh_token_info(payload)

    def login(self, user: User):
        user_jwt = create_token_info(user)
        self._user_jwt = user_jwt
        self.set_user_jwt(user_jwt)

    def logout(self) -> None:
        # todo. add to blacklist in Redis
        ...

    def is_authenticated(self) -> bool:
        if self._user_jwt:
            payload = decode_jwt(self._user_jwt.access_token)
            if payload:
                return True
        return False
