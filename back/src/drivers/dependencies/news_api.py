from fastapi import Depends, Request, Response
from typing import Annotated

from src.infrastructure.repository.news.news import NewsFilterRepository
from src.infrastructure.adapters.news.news_api import NewsAdapter
from src.infrastructure.services.db.db import AsyncSession, db_helper
from src.infrastructure.services.aiohttp.engine import engine


async def get_news_filter_repo(
    session: AsyncSession = Depends(db_helper.get_session),
) -> NewsFilterRepository:
    return NewsFilterRepository(session)


async def get_news_adapter():
    return NewsAdapter(await engine.get_session())


NewsDep = Annotated[NewsAdapter, Depends(get_news_adapter)]
FilterRepoDep = Annotated[NewsFilterRepository, Depends(get_news_filter_repo)]
