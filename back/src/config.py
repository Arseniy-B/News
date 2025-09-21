from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    API_KEY: str
    BASE_API_URL: str = "https://newsapi.org/v2/"

    @property
    def get_url(self):
        return f"https://newsapi.org/v2/everything?q=tesla&from=2025-08-19&sortBy=publishedAt&language=ru&apiKey={self.API_KEY}"

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env')


config = Config() # pyright: ignore
