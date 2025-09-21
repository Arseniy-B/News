from src.domain.port.news_api import NewsClient, NewsFilter, NewsResponse


async def get_news(news_client: NewsClient, filters: NewsFilter | None = None) -> NewsResponse:
    news = await news_client.get_news(filters)
    return news
