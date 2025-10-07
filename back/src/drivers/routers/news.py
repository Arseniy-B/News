from fastapi import APIRouter, Depends
from src.use_cases.get_news import get_news
from src.infrastructure.adapters.news.news_api import NewsAdapter, engine
from src.infrastructure.adapters.news.schemas.filter import TopHeadlinesFilter


router = APIRouter(prefix="/news")


@router.post("/get")
async def get_news_endpoint(filters: TopHeadlinesFilter | None):
    return await get_news(NewsAdapter(await engine.get_session()), filters)
