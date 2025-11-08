from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import json

from src.drivers.dependencies.cache import cache
from src.infrastructure.adapters.news.news_api import create_news_adapter
from src.use_cases.get_news import get_news
from src.infrastructure.exceptions import NewsRepoError
from src.domain.exceptions import ValidationError
from src.infrastructure.adapters.news.schemas.news import NewsResponse


router = APIRouter(prefix="/news")


@router.post("/get")
@cache(10)
async def get_news_endpoint(filters_dict: dict[str, Any], news_type: str):
    try:
        news_adapter = await create_news_adapter(news_type=news_type, data=filters_dict)
        news = await get_news(news_adapter)
    except (ValidationError, NewsRepoError) as e:
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": str(e)
        }

    if not isinstance(news, NewsResponse):
        raise NewsRepoError

    return JSONResponse({"data": json.loads(news.model_dump_json())}, status_code=status.HTTP_200_OK)
