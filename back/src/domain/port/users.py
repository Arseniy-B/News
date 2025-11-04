from abc import ABC, abstractmethod
from src.domain.entities.user import User, UserCreate, UserLogin
from src.domain.entities.news import NewsFilters
from typing import Type, Sequence


class UserPort(ABC):
    @abstractmethod
    async def set_news_filters(self, filters: NewsFilters, user_id: int):
        ...

    @abstractmethod
    async def get_news_filters(self,  user_id: int, filter_type: Type[NewsFilters] | None = None) -> Sequence[NewsFilters]:
        ...

    @abstractmethod
    async def create(self, user_create: UserCreate) -> User:
        pass

    @abstractmethod
    async def update(self, user_update: User):
        pass

    @abstractmethod
    async def get_by_login(self, user_login: UserLogin) -> User | None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        pass
    
    @abstractmethod
    async def get_by_email(self, user_email: str) -> User | None:
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
    def get_user_id(self) -> int | None:
        pass
