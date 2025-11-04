from src.domain.port.users import AuthPort, UserLogin as ABCUserLogin, UserPort, User
from src.infrastructure.adapters.auth.self_auth.auth import AuthAdapter


class GmailAuthAdapter(AuthAdapter, AuthPort):
    async def authenticate(self, user_login: ABCUserLogin, user_repo: UserPort) -> User:
        ...
