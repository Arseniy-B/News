from src.domain.port.users import UserAuthId as ABCUserAuthId, UserRepo
from src.domain.entities.user import User


class UserAuthId(ABCUserAuthId):
    access_token: str
    refresh_token: str


class UserAdapter(UserRepo):
    async def login(self, User):
        pass

    async def logout(self, user_id: str) -> None:
        pass

    async def is_authenticated(self, User):
        pass
