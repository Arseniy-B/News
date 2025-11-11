from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.infrastructure.services.db.models import UserModel
from src.infrastructure.repository.users.utils.password import (
    hash_password,
    validate_password,
)
from src.infrastructure.exceptions import UserRepoError, UserNotFound
from src.domain.entities.user import User, UserCreate as ABCUserCreate
from src.domain.port.users import UserPort
from src.infrastructure.repository.users.schemas import UserCreate


class UserRepository(UserPort):
    def __init__(self, session: AsyncSession):
        self._session = session

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

    async def get_by_username(self, username: str) -> User:
        stmt = select(UserModel).where(UserModel.username == username)
        user = await self._session.scalar(stmt)
        if not user:
            raise UserNotFound
        return UserRepository.transform_to_user(user)

    async def get_by_email(self, user_email: str) -> User:
        stmt = select(UserModel).where(UserModel.email == user_email)
        user = await self._session.scalar(stmt)
        if not user:
            raise UserNotFound
        return UserRepository.transform_to_user(user)

    async def get_by_id(self, user_id: int) -> User:
        user = await self._session.get(UserModel, user_id)
        if not user:
            raise UserNotFound
        return self.transform_to_user(user)

    async def create(self, user_create: ABCUserCreate):
        if not isinstance(user_create, UserCreate):
            raise UserRepoError
        try:
            user = UserModel(
                username=user_create.username,
                email=user_create.email,
                password_hash=hash_password(user_create.password),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            self._session.add(user)
        except IntegrityError:
            raise 
        await self._session.commit()

    async def update(self, user_update: User):
        ...
        # user_model = self._session.get(UserModel, user_update.id)
        # for field in fields(user_update):
        #     value = getattr(user_update, field.name)
        #     setattr(user_model, str(field), value)
        # await self._session.commit()
