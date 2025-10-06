from abc import ABC, abstractmethod
from src.domain.entities.user import User, UserCreate, UserLogin



class UserRepository(ABC):
    @abstractmethod
    async def create(self, user_create: UserCreate) -> User:
        pass

    @abstractmethod
    async def update(self, user_update: User):
        pass

    @abstractmethod
    async def get_by_login(self, user_login: UserLogin) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

class AuthRepository(ABC):
    @abstractmethod
    async def login(self, user):
        pass

    @abstractmethod
    async def logout(self):
        pass

    @abstractmethod
    async def is_authenticated(self) -> bool:
        pass

