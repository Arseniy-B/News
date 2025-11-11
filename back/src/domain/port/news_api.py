from abc import ABC, abstractmethod
from src.domain.entities.news import NewsFilter, News, NewsResponse
from typing import Sequence


class NewsApiPort(ABC):
    @abstractmethod
    async def get_news_list(self, news_filter: NewsFilter) -> NewsResponse:
        pass

    
class NewsFilterPort(ABC):
    @abstractmethod
    async def save(self, user_id: int, news_filter: NewsFilter):
        pass

    @abstractmethod
    async def get_by_type(self, user_id: int, filter_types: list[str]) -> Sequence[NewsFilter]:
        pass
