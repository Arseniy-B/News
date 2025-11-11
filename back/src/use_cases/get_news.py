from src.domain.port.news_api import NewsApiPort
from src.domain.entities.news import NewsResponse, NewsFilter


async def get_news(news_port: NewsApiPort, filter: NewsFilter) -> NewsResponse:
    news_list = await news_port.get_news_list(filter)
    return news_list
