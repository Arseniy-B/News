from abc import ABC, abstractmethod
from src.domain.entities.user import User


class UserAuthId(ABC):
    pass

class UserCreate(ABC):
    pass

class UserLogin(ABC):
    pass


class UserRepo(ABC):
    @abstractmethod
    async def create(self, user) -> User:
        pass

    @abstractmethod
    async def login(self, user) -> UserAuthId:
        pass

    @abstractmethod
    async def logout(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def is_authenticated(self, user_auth_id: UserAuthId) -> bool:
        pass

