from src.domain.entities.user import User, UserCreate, UserLogin
from src.use_cases.exceptions import UserNotFound, InvalidCredentials, DublicateEntityError
from src.domain.port.users import AuthRepository, UserRepository


async def registration(user_create: UserCreate, user_repo: UserRepository) -> User:
    if await user_repo.get_by_email(user_create.email):
        raise DublicateEntityError("user")
    user = await user_repo.create(user_create)
    if not user:
        raise UserNotFound
    return user


async def login(
    user_login: UserLogin, auth_repo: AuthRepository, user_repo: UserRepository
):
    user = await user_repo.get_by_login(user_login)
    if not user:
        raise InvalidCredentials
    if not user_repo.verify_password(user_login.password, user.password_hash):
        raise InvalidCredentials

    auth_repo.login(user)
