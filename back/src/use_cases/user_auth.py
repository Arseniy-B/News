from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.port.users import AuthPort, UserPort
from src.use_cases.exceptions import (
    InvalidCredentials,
    UserNotFound,
    UserNotAuthorized
)


async def registration(user_create: UserCreate, user_repo: UserPort) -> User:
    user = await user_repo.create(user_create)
    if not user:
        raise UserNotFound
    return user


async def login(
    user_login: UserLogin, auth_repo: AuthPort, user_repo: UserPort
):
    user = await auth_repo.authenticate(user_login, user_repo)
    if not user:
        raise InvalidCredentials
    auth_repo.login(user)


async def logout(
    auth_repo: AuthPort,
):
    if not auth_repo.is_authenticated():
        raise UserNotAuthorized
    await auth_repo.logout()

