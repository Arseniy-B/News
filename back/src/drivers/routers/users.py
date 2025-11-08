from typing import Any

from dataclasses import asdict
from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

from src.drivers.dependencies.user import AuthRepoDep, UserRepoDep
from src.infrastructure.adapters.news.news_api import create_news_adapter, news_types
from src.use_cases.action_on_user import get_user_data
from src.use_cases.exceptions import (
    UserNotAuthorized,
    UserNotFound,
)
from src.use_cases.user_news import get_user_filters, set_user_filters

router = APIRouter(prefix="/user")


@router.post("/set-filters")
async def set_news_filters(
    user_repo: UserRepoDep,
    auth_repo: AuthRepoDep,
    news_type: str,
    data: dict[str, Any],
):
    news_adapter = await create_news_adapter(news_type, data)
    await set_user_filters(user_repo, auth_repo, news_adapter)
    return JSONResponse(
        {"detail": "filters were saved"}, status_code=status.HTTP_200_OK
    )


@router.post("/get-filters")
async def get_news_filters(
    user_repo: UserRepoDep,
    auth_repo: AuthRepoDep,
    news_type_name: str | None = None,
):
    news_type = None
    if news_type_name in news_types:
        news_type = news_types[news_type_name]
    data = await get_user_filters(user_repo, auth_repo, news_type)
    return JSONResponse({"data": data}, status_code=status.HTTP_200_OK)


@router.get("/get")
async def get_user_endpoint(auth_repo: AuthRepoDep, user_repo: UserRepoDep):
    try:
        user = await get_user_data(user_repo, auth_repo)
    except (UserNotFound):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    d = asdict(user)
    for key, value in d.items():
        if isinstance(value, datetime):
            d[key] = value.isoformat()
    return JSONResponse({"data": d}, status_code=status.HTTP_200_OK)
