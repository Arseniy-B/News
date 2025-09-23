from src.domain.port.users import UserAuthId as ABCUserAuthId, UserRepo
from src.domain.entities.user import User

import jwt


class UserAuthId(ABCUserAuthId):
    access_token: str
    refresh_token: str


class UserAdapter(UserRepo):
    def __init__(self, session: None = None):
        ...

    async def create(self, User):
        ...

    async def login(self, User) -> UserAuthId:
        ...


    async def logout(self, UserAuthId) -> None:
        ...


    async def is_authenticated(self, UserAuthId) -> bool:
        ...
