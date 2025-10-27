from abc import ABC, abstractmethod
from src.domain.entities.news import NewsFilters, News, NewsResponse
from typing import Sequence, Any


class NewsPort(ABC):
    @abstractmethod
    async def get_news_list(self) -> NewsResponse:
        pass

    @abstractmethod
    def get_filters(self) -> NewsFilters:
        pass

    @staticmethod
    @abstractmethod
    async def create(filters_dict: dict[str, Any]) -> 'NewsPort':
        pass
