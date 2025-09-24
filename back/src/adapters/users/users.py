from src.domain.port.users import UserAuthId as ABCUserAuthId, UserRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.adapters.db.db import db_helper
from src.adapters.db.models import Users as UserModel
from src.adapters.users.schemas import *
from src.adapters.users.utils.password import *
from src.adapters.users.utils.jwt import *
from pydantic import BaseModel



class UserAdapter(UserRepo):
    def __init__(self, session: AsyncSession):
        self._session = session


    @staticmethod
    async def transform_to_user(user: UserModel) -> User:
        return User(
            id=user.id,
            username=user.username,
            password_hash=user.password,
        )

    async def get(self, user_login: UserLogin) -> User:
        stmt = select(UserModel).where(UserModel.username == user_login.login)
        user = await self._session.scalar(stmt)
        if not user:
            raise 
        return await UserAdapter.transform_to_user(user)


    async def check_password_strength(self, password: str) -> bool:
        return True


    async def create(self, user_create: UserCreate) -> User:
        user = UserModel(
            username=user_create.login, 
            password=hash_password(user_create.password1)
        )
        return await UserAdapter.transform_to_user(user)


    async def login(self, user: User) -> UserAuthId:
        return await create_token_info(user)


    async def logout(self, auth_id: UserAuthId) -> None:
        #Add to blacklist in Redis
        ...


    async def is_authenticated(self, auth_id: UserAuthId) -> bool:
        payload = decode_jwt(UserAuthId.access_token)
        if payload:
            return True
        return False

