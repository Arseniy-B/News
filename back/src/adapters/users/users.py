from src.domain.port.users import UserAuthId as ABCUserAuthId, UserRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.entities.user import User
from src.adapters.db.db import db_helper
from src.adapters.news.news_api import BaseFilter
from src.adapters.db.models import Users as UserModel
from src.adapters.users.schemas import *
from src.adapters.users.utils.password import *
from src.adapters.users.utils.jwt import *
from src.adapters.news.news_api import NewsAdapter
from pydantic import BaseModel
from dataclasses import fields



class UserAdapter(UserRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    async def transform_to_user(user: UserModel) -> User:
        domain_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
        )
        if user.news_filters:
            filters = await NewsAdapter.parse_dict_to_filters(user.news_filters) 
            domain_user.news_filters = filters
        return domain_user


    async def get_by_login(self, user_login: UserLogin) -> User:
        stmt = select(UserModel).where(UserModel.username == user_login.login)
        user = await self._session.scalar(stmt)
        if not user:
            raise 
        return await UserAdapter.transform_to_user(user)

    async def get_by_id(self, user_id: int) -> UserModel:
        user = await self._session.get(UserModel, user_id)
        if not user:
            raise
        return user


    async def check_password_strength(self, password: str) -> bool:
        return True


    async def create(self, user_create: UserCreate) -> User:
        user = UserModel(
            username=user_create.login, 
            email='',
            password_hash=hash_password(user_create.password1),
            news_filters=dict()
        )
        self._session.add(user)
        await self._session.commit()
        return await UserAdapter.transform_to_user(user)


    async def update(self, user: User):
        user_model = self.get_by_id(user.id)
        for field in fields(user):
            value = getattr(user, field.name)
            setattr(user_model, str(field), value)
        await self._session.commit()


    async def login(self, user: User) -> UserAuthId:
        return await create_token_info(user)


    async def logout(self, auth_id: UserAuthId) -> None:
        #todo. add to blacklist in Redis
        ...


    async def is_authenticated(self, auth_id: UserAuthId) -> bool:
        payload = decode_jwt(auth_id.access_token)
        if payload:
            return True
        return False

