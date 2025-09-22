from fastapi import APIRouter, Depends, Request
from src.use_cases.news_api import get_news
from src.adapters.news.news_api import NewsAdapter, engine
from src.adapters.news.schemas.filter import *
from src.drivers.dependencies.auth import login_required


router = APIRouter(prefix="/news", dependencies=[Depends(login_required)])


@router.post('/get')
async def get_news_endpoint(filters: TopHeadlinesFilter | None):
    return await get_news(NewsAdapter(await engine.get_session()), filters)


@router.get("/test")
async def test(request: Request):
    ...

