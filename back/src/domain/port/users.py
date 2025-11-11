from abc import ABC, abstractmethod
from src.domain.entities.user import User, UserLogin, UserCreate


class UserPort(ABC):
    @abstractmethod
    async def create(self, user_create: UserCreate):
        pass

    @abstractmethod
    async def update(self, user_update: User):
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        pass
    
    @abstractmethod
    async def get_by_email(self, user_email: str) -> User:
        pass


class AuthPort(ABC):
    @abstractmethod
    def login(self, user):
        pass

    @abstractmethod
    async def logout(self):
        pass

    @abstractmethod
    async def authenticate(self, user_login: UserLogin, user_repo: UserPort) -> User:
        pass

    @abstractmethod
    async def is_authenticated(self) -> bool:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass
