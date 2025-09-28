from abc import ABC, abstractmethod
from src.domain.entities.user import User
from dataclasses import dataclass


@dataclass
class UserAuthId(ABC):
    pass

@dataclass
class UserCreate(ABC):
    login: str
    password1: str
    password2: str


@dataclass
class UserLogin(ABC):
    login: str
    password: str


class UserRepo(ABC):
    @abstractmethod
    async def create(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    async def check_password_strength(self, password: str) -> None:
        pass

    @abstractmethod
    async def get_by_login(self, user_login: UserLogin) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    async def login(self, user) -> UserAuthId:
        pass

    @abstractmethod
    async def logout(self, user: User) -> UserAuthId:
        pass

    @abstractmethod
    async def is_authenticated(self, user_auth_id: UserAuthId) -> bool:
        pass

