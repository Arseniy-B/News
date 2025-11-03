from typing import Any

from fastapi import APIRouter, status

from src.drivers.dependencies.cache import cache
from src.infrastructure.adapters.news.news_api import create_news_adapter
from src.use_cases.get_news import get_news
from src.infrastructure.exceptions import NewsRepoError
from src.domain.exceptions import ValidationError


router = APIRouter(prefix="/news")


@router.post("/get")
@cache(10)
async def get_everything_news_endpoint(filters_dict: dict[str, Any], news_type: str):
    try:
        news_adapter = await create_news_adapter(news_type=news_type, data=filters_dict)
        news = await get_news(news_adapter)
    except (ValidationError, NewsRepoError) as e:
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": str(e)
        }
    return {"status_code": 200, "data": news}
