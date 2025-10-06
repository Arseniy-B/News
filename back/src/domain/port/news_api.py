from abc import ABC, abstractmethod
from src.domain.entities.news import NewsFilter, News


class NewsClient(ABC):
    @abstractmethod
    async def get_news_list(self, filter: NewsFilter | None) -> list[News]:
        pass
