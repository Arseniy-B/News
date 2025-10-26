from typing import Any

from fastapi import APIRouter, status

from src.drivers.dependencies.cache import cache
from src.infrastructure.adapters.news.news_api import TopHeadlinesNewsAdapter, EverythingNewsAdapter
from src.use_cases.get_news import get_news
from src.infrastructure.exceptions import NewsRepoError
from src.domain.exceptions import ValidationError


router = APIRouter(prefix="/news")


@router.post("/everything")
@cache(10)
async def get_everything_news_endpoint(filters_dict: dict[str, Any]):
    try:
        news_adapter = await EverythingNewsAdapter.create(filters_dict)
        news = await get_news(news_adapter)
    except ValidationError as e:
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": str(e)
        }
    return {"status_code": 200, "data": news}


@router.post("/top-headlines")
@cache(10)
async def get_top_headlines_news_endpoint(filters_dict: dict[str, Any]):
    try:
        news_adapter = await TopHeadlinesNewsAdapter.create(filters_dict)
        news = await get_news(news_adapter)
    except ValidationError as e:
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": str(e)
        }
    return {"status_code": 200, "data": news}

