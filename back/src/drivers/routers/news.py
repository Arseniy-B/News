from fastapi import APIRouter
from src.use_cases.news_api import get_news
from src.adapters.news_api import NewsAdapter, engine
from src.adapters.schemas.filter import *


router = APIRouter()

@router.post('/news/get/')
async def get_news_endpoint(filters: TopHeadlinesFilter | None):
    return await get_news(NewsAdapter(await engine.get_session()), filters)

