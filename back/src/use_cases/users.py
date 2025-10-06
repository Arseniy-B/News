import re

from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.exceptions import UserNotFound
from src.domain.port.users import UserRepository, AuthRepository


async def registration(user_create: UserCreate, user_repo: UserRepository) -> User:
    user = await user_repo.create(user_create)
    if not user:
        raise UserNotFound
    return user


async def login(user_login: UserLogin, auth_repo: AuthRepository, user_repo: UserRepository):
    user = await user_repo.get_by_login(user_login)
    if not user:
        raise UserNotFound
    await auth_repo.login(user)
