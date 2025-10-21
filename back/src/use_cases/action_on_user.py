from src.domain.port.users import AuthRepository, UserRepository
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound
from src.domain.entities.user import User


async def get_user_data(user_repo: UserRepository, auth_repo: AuthRepository) -> User:
    if not auth_repo.is_authenticated():
        raise UserNotAuthorized

    id = auth_repo.get_user_id()
    if not id:
        raise UserNotAuthorized

    user = await user_repo.get_by_id(id)
    if not user:
        raise UserNotFound
    return user
