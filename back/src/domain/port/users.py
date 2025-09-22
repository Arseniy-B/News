from abc import ABC, abstractmethod


class UserAuthId(ABC):
    pass


class UserRepo(ABC):
    @abstractmethod
    async def create(self, user):
        pass

    @abstractmethod
    async def login(self, user):
        pass

    @abstractmethod
    async def logout(self, user_id: str) -> None:
        pass

    @abstractmethod
    async def is_authenticated(self, user_auth_id: UserAuthId):
        pass

