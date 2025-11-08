from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.port.users import AuthPort, UserPort
from src.domain.port.email import EmailPort
from src.use_cases.exceptions import (
    InvalidCredentials,
    UserNotFound,
    UserNotAuthorized,
    ClienValidationError,
    DublicateEntityError
)

async def registration(user_create: UserCreate, user_repo: UserPort):
    try:
        await user_repo.create(user_create)
    except DublicateEntityError:
        raise ClienValidationError("email", "such user already exists")

async def login(
    user_login: UserLogin, auth_repo: AuthPort, user_repo: UserPort
):
    try:
        user = await auth_repo.authenticate(user_login, user_repo)
    except UserNotFound:
        raise InvalidCredentials
    auth_repo.login(user)
