from src.domain.port.news_api import NewsClient
from src.domain.entities.news import News, NewsFilter


async def get_news(
    news_client: NewsClient, filters: NewsFilter | None = None
) -> list[News]:
    news_list = await news_client.get_news_list(filters)
    return news_list
