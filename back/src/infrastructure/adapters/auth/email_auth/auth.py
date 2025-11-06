from src.domain.entities.user import User
from src.domain.entities.user import UserLogin as ABCUserLogin
from src.domain.port.users import AuthPort, UserPort
from src.infrastructure.adapters.auth.self_auth.auth import AuthAdapter
from src.infrastructure.exceptions import AuthRepoError
from src.infrastructure.adapters.auth.email_auth.schemas import UserLogin
from src.infrastructure.services.redis.redis import redis_helper
from src.use_cases.exceptions import InvalidCredentials
from src.infrastructure.adapters.email.email import EmailAdapter
from src.domain.utils.otp import generate_otp_code
from src.config import config


class EmailAuthAdapter(AuthAdapter, AuthPort):
    def _get_redis_key(self, email, code):
        return f"{email}:{code}"

    async def authenticate(self, user_login: ABCUserLogin, user_repo: UserPort) -> User:
        if not isinstance(user_login, UserLogin):
            raise AuthRepoError

        redis = await redis_helper.get_redis()
        if not await redis.get(self._get_redis_key(user_login.email, user_login.code)):
            raise InvalidCredentials

        user = await user_repo.get_by_email(user_login.email)
        if not user:
            raise AuthRepoError
        return user

    async def send_code(self, email):
        otp = generate_otp_code()
        redis = await redis_helper.get_redis()
        redis.set(self._get_redis_key(email, otp), "", ex=config.otp.expire_minutes * 60)
        await EmailAdapter().send_otp(email, otp)
