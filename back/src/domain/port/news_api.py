from abc import ABC, abstractmethod


class News(ABC):
    pass


class NewsResponse():
    news: list[News]


class NewsFilter(ABC):
    pass


class NewsClient(ABC):
    @abstractmethod
    async def get_news(self, NewsFilter) -> NewsResponse:
        pass

