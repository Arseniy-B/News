from src.domain.port.news_api import NewsClient
from src.domain.entities.news import News, NewsFilter
from typing import Sequence


async def get_news(
    news_client: NewsClient, filters: NewsFilter | None = None
) -> Sequence[News]:
    news_list = await news_client.get_news_list(filters)
    print(news_list)
    return news_list
