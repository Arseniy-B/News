from typing import Any

from pydantic import BaseModel
from dataclasses import asdict
from fastapi import APIRouter, Depends, Request, status, Body
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

from src.drivers.dependencies.user import AuthRepoDep, UserRepoDep
from src.drivers.dependencies.news_api import FilterRepoDep
from src.infrastructure.adapters.news.news_api import NewsAdapter
from src.use_cases.action_on_user import get_user_data
from src.use_cases.exceptions import (
    UserNotAuthorized,
    UserNotFound,
)
from src.use_cases.user_news import get_user_filter, set_user_filter

router = APIRouter(prefix="/user")


@router.post("/set-filters")
async def set_news_filters(
    auth_repo: AuthRepoDep,
    filter_repo: FilterRepoDep,
    filter_type: str,
    data: dict[str, Any] = Body(...),
):
    filter_model = filter_repo.get_filter_by_type(filter_type)
    news_filter = filter_model.model_validate(data)
    await set_user_filter(auth_repo, news_filter, filter_repo)
    return JSONResponse(
        {"detail": "filters were saved"}, status_code=status.HTTP_200_OK
    )


@router.post("/get-filters")
async def get_news_filters(
    auth_repo: AuthRepoDep,
    filter_repo: FilterRepoDep,
    filter_types: list[str] = Body(...),
):
    data = await get_user_filter(auth_repo, filter_repo, filter_types)
    return JSONResponse({"data": [i.__dict__ for i in data]}, status_code=status.HTTP_200_OK)


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
