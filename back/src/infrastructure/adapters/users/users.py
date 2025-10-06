from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.services.db.models import Users as UserModel
from src.infrastructure.adapters.news.news_api import NewsAdapter
from src.infrastructure.adapters.users.utils.password import hash_password
from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.port.users import UserRepository


class UserAdapter(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    async def transform_to_user(user: UserModel) -> User:
        domain_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        if user.news_filters:
            filters = await NewsAdapter.parse_dict_to_filters(user.news_filters)
            domain_user.news_filters = filters
        return domain_user

    async def get_by_login(self, user_login: UserLogin) -> User:
        stmt = select(UserModel).where(UserModel.username == user_login.username)
        user = await self._session.scalar(stmt)
        if not user:
            raise
        return await UserAdapter.transform_to_user(user)

    async def get_by_id(self, user_id: int) -> User:
        user = await self._session.get(UserModel, user_id)
        if not user:
            raise
        return await self.transform_to_user(user)

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
        return await UserAdapter.transform_to_user(user)

    async def update(self, user_update: User):
        ...
        # user_model = self._session.get(UserModel, user_update.id)
        # for field in fields(user_update):
        #     value = getattr(user_update, field.name)
        #     setattr(user_model, str(field), value)
        # await self._session.commit()
