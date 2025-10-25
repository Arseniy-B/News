from src.domain.port.news_api import NewsPort
from src.domain.entities.news import News
from typing import Sequence


async def get_news(
    news_port: NewsPort
) -> Sequence[News]:
    news_list = await news_port.get_news_list()
    return news_list
