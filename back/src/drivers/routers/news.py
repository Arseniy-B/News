from typing import Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import json

from src.drivers.dependencies.cache import cache
from src.use_cases.get_news import get_news
from src.infrastructure.exceptions import NewsRepoError
from src.domain.exceptions import ValidationError
from src.infrastructure.adapters.news.schemas.news import NewsResponse
from src.infrastructure.repository.news.news import NewsFilterRepository
from src.drivers.dependencies.news_api import NewsDep



router = APIRouter(prefix="/news")


@router.post("/get")
@cache(10)
async def get_news_endpoint(
    filter_dict: dict[str, Any],
    filter_type: str,
    news_adapter: NewsDep,
):
    filter_model = NewsFilterRepository.get_filter_by_type(filter_type)
    news_filter = filter_model.model_validate(filter_dict)
    try:
        news = await get_news(news_adapter, news_filter)
    except (ValidationError, NewsRepoError) as e:
        return {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "detail": str(e)
        }

    if not isinstance(news, NewsResponse):
        raise NewsRepoError

    return JSONResponse({"data": json.loads(news.model_dump_json())}, status_code=status.HTTP_200_OK)
