from abc import ABC, abstractmethod
from src.domain.utils.otp import Otp


OtpStorageKey = str

class OtpStoragePort(ABC):
    @abstractmethod
    def save_otp(self, key: OtpStorageKey, otp: Otp, ttl: int = 300) -> None: 
        pass

    @abstractmethod
    def verify_otp(self, key: OtpStorageKey, otp: Otp) -> bool: 
        pass
