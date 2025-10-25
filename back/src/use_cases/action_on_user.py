from src.domain.port.users import AuthPort, UserPort
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound
from src.domain.entities.user import User


async def get_user_data(user_port: UserPort, auth_port: AuthPort) -> User:
    if not auth_port.is_authenticated():
        raise UserNotAuthorized

    id = auth_port.get_user_id()
    if not id:
        raise UserNotAuthorized

    user = await user_port.get_by_id(id)
    if not user:
        raise UserNotFound
    return user
