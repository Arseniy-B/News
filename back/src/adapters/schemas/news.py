from src.domain.port.news_api import News as ABCNews, NewsResponse as ABCNewsResponse
from src.domain.exceptions import *
from pydantic import BaseModel, model_validator

from datetime import datetime
from typing import Any
from enum import Enum


class Source(BaseModel):
    id: str | None
    name: str | None


class News(BaseModel, ABCNews):
    source: Source
    author: str | None = None
    title: str
    description: str | None
    url: str | None
    urlToImage: str | None
    publishedAt: datetime 
    content: str | None


class Status(Enum):
    OK = "ok"
    ERROR = "error"


class NewsResponse(BaseModel, ABCNewsResponse):
    news: list[News]
    status: Status
    totalResults: int

    @model_validator(mode="before")
    def validate(cls, data: Any):
        if not data: 
            raise ValidationError("empty data")
        if data['status'] == Status.ERROR:
            raise ValidationError(f"code: {data['code']}, message: {data['message']}")

        data['news'] = data['articles']
        print(data)
        
        return data
