from fastapi import Request, Response
from src.infrastructure.adapters.auth.schemas import UserJWT
from src.infrastructure.adapters.auth.utils.jwt import create_token_info, decode_jwt
from src.domain.port.users import AuthRepository

from src.config import config
from src.domain.entities.user import User


class AuthAdapter(AuthRepository):
    def __init__(self, request: Request, response: Response):
        self._request = request
        self._response = response
        self._user_jwt = self.get_user_jwt()

    async def set_user_jwt(self, user_jwt: UserJWT):
        conf = {
            "httponly": True,
            "secure": True,  # только по HTTPS
            "samesite": "none",  # защита от CSRF
            "max_age": config.auth_jwt.refresh_token_expire_minutes,
        }

        self._response.set_cookie(
            key="refresh_token", value=user_jwt.refresh_token, **conf
        )
        self._response.headers["Authorization"] = f"Bearer {user_jwt.access_token}"

    def get_user_jwt(self) -> UserJWT | None:
        access_token = self._request.headers["Authorization"]
        refresh_token = self._request.cookies.get("refresh_token")

        access_token = access_token.split()
        if access_token[0] != "Bearer":
            raise
        access_token = access_token[1]

        if refresh_token and access_token:
            user_jwt = UserJWT(access_token=access_token, refresh_token=refresh_token)
            return user_jwt
        return None

    # async def refresh_token(self, refresh_token: str):
    #     payload = decode_jwt(refresh_token)
    #     user = await self._session.get(UserModel, int(payload.sub))
    #     if not user:
    #         raise UserNotFound
    #     self._user_jwt = await create_token_info(await self.transform_to_user(user))

    async def login(self, user: User):
        user_jwt = await create_token_info(user)
        self._user_jwt = user_jwt
        await self.set_user_jwt(user_jwt)

    async def logout(self) -> None:
        # todo. add to blacklist in Redis
        ...

    async def is_authenticated(self) -> bool:
        if self._user_jwt:
            payload = decode_jwt(self._user_jwt.access_token)
            if payload:
                return True
        return False
