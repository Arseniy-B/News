from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.services.db.models import Users as UserModel
from src.infrastructure.adapters.news.news_api import NewsAdapter
from src.infrastructure.repository.users.utils.password import hash_password, validate_password
from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.port.users import UserPort
from src.domain.entities.news import NewsFilters


class UserRepository(UserPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def set_news_filters(self, filters: NewsFilters, user_id: int):
        ...

    async def get_news_filters(self, user_id: int) -> NewsFilters:
        ...

    def verify_password(self, password: str, password_hash: str) -> bool:
        return validate_password(password, password_hash)

    @staticmethod
    def transform_to_user(user: UserModel) -> User:
        domain_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        return domain_user

    async def get_by_login(self, user_login: UserLogin) -> User | None:
        stmt = select(UserModel).where(UserModel.username == user_login.username)
        user = await self._session.scalar(stmt)
        if user:
            return UserRepository.transform_to_user(user)

    async def get_by_email(self, user_email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == user_email)
        user = await self._session.scalar(stmt)
        if user:
            return UserRepository.transform_to_user(user)

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self._session.get(UserModel, user_id)
        if user:
            return self.transform_to_user(user)

    async def create(self, user_create: UserCreate) -> User:
        user = UserModel(
            username=user_create.username,
            email=user_create.email,
            password_hash=hash_password(user_create.password),
            updated_at=datetime.now(),
            created_at=datetime.now(),
        )
        self._session.add(user)
        await self._session.commit()
        return UserRepository.transform_to_user(user)

    async def update(self, user_update: User):
        ...
        # user_model = self._session.get(UserModel, user_update.id)
        # for field in fields(user_update):
        #     value = getattr(user_update, field.name)
        #     setattr(user_model, str(field), value)
        # await self._session.commit()
