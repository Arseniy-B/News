from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30


class BaseDbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    db_echo: bool = True

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class BaseNewsApiSettings(BaseSettings):
    API_KEY: str
    BASE_API_URL: str = "https://newsapi.org/v2/"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def get_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class EmailSettings(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    def get_otp_content(self, otp) -> str:
        return f"Your login code: {otp}"

    def get_welcome_content(self) -> str:
        return "welcome"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class Otp(BaseSettings):
    expire_minutes: int = 5


class Config:
    news_api = BaseNewsApiSettings()  # pyright: ignore
    db = BaseDbSettings()  # pyright: ignore
    auth_jwt = AuthJWT()
    redis = RedisSettings()  # pyright: ignore
    email = EmailSettings()  # pyright: ignore
    otp = Otp()


config = Config()  # pyright: ignore
