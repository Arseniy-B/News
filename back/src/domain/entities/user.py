from dataclasses import dataclass
from src.domain.port.news_api import NewsFilter


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    email: str | None = None
    news_filters: NewsFilter | None = None

