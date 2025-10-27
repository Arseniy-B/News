from src.domain.port.news_api import NewsPort
from src.domain.entities.news import News, NewsResponse


async def get_news(news_port: NewsPort) -> NewsResponse:
    news_list = await news_port.get_news_list()
    return news_list
