from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.services.db.models import UserModel, NewsFiltersModel
from src.infrastructure.repository.users.utils.password import hash_password, validate_password
from src.infrastructure.exceptions import UserRepoError
from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.entities.news import NewsFilters
from src.domain.port.users import UserPort
from src.infrastructure.adapters.news.schemas.filter import BaseFilter
from typing import Type, Sequence


class UserRepository(UserPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_news_filters(self, user_id: int , filter_type: Type[NewsFilters] | None = None) -> Sequence[NewsFilters]:
        if filter_type and not issubclass(filter_type, BaseFilter):
            raise UserRepoError
        stmt = select(NewsFiltersModel).where(NewsFiltersModel.user_id == user_id)
        if filter_type:
            stmt = stmt.where(NewsFiltersModel.filter_type == filter_type.__name__)
        result = await self._session.execute(stmt)

        if filter_type:
            return [filter_type.model_validate(result)]
        return [BaseFilter.model_validate(i) for i in result]

    async def set_news_filters(self, filters: NewsFilters, user_id: int):
        if not isinstance(filters, BaseFilter):
            raise UserRepoError
        await self._session.execute(
            delete(NewsFiltersModel).where(NewsFiltersModel.user_id == user_id,
            NewsFiltersModel.filter_type == filters.__class__.__name__)
        )
        filter_type = filters.__class__.__name__
        data = filters.model_dump(exclude_unset=True, exclude_none=True)
        new_filter = NewsFiltersModel(
            user_id=user_id,
            filter_type=filter_type,
            data=data
        )
        self._session.add(new_filter)
        await self._session.commit()


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
