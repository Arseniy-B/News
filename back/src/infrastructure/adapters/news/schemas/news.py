from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, model_validator

from src.domain.exceptions import ValidationError
from src.domain.port.news_api import News as ABCNews


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


class NewsResponse(BaseModel):
    news: list[ABCNews]
    status: Status
    totalResults: int

    @model_validator(mode="before")
    def validate_all_fields(cls, data: Any):
        if not data:
            raise ValidationError("empty data")
        if data["status"] == Status.ERROR:
            raise ValidationError(f"code: {data['code']}, message: {data['message']}")
        data["news"] = data["articles"]
        return data
