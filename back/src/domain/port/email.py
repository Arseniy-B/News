from abc import ABC, abstractmethod
from src.domain.utils.otp import Otp


class EmailPort(ABC):
    @abstractmethod
    async def send_otp(self, email: str, otp: Otp):
        pass

    @abstractmethod
    async def send_welcome(self, email: str):
        pass

