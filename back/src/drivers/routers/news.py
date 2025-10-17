from typing import Any

from fastapi import APIRouter, Depends

from src.drivers.dependencies.cache import cache
from src.infrastructure.adapters.news.news_api import NewsAdapter, engine
from src.infrastructure.adapters.news.schemas.filter import TopHeadlinesFilter
from src.infrastructure.services.redis.redis import redis_helper
from src.use_cases.get_news import get_news


router = APIRouter(prefix="/news")


@router.post("/get")
@cache(60)
async def get_news_endpoint(filters_dict: dict[str, Any] | None):
    filters = None
    if filters_dict:
        filters = TopHeadlinesFilter(**filters_dict)
    return await get_news(NewsAdapter(await engine.get_session()), filters)
