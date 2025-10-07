from abc import ABC, abstractmethod
from src.domain.entities.news import NewsFilter, News
from typing import Sequence


class NewsClient(ABC):
    @abstractmethod
    async def get_news_list(self, filter: NewsFilter | None) -> Sequence[News]:
        pass
