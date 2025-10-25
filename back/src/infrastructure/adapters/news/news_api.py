from http import HTTPStatus
from typing import Any, Sequence
from urllib.parse import urlencode
from pydantic import ValidationError as PydanticValidationError

import aiohttp

from src.config import config
from src.domain.entities.news import News, NewsFilters
from src.domain.port.news_api import NewsPort
from src.infrastructure.adapters.news.schemas.filter import (
    BaseFilter,
    EverythingFilters,
    TopHeadlinesFilter,
)
from src.infrastructure.adapters.news.schemas.news import NewsResponse
from src.infrastructure.exceptions import (
    FilterSchemaNotFound,
    NewsRepoError,
    ValidationError,
)
from src.infrastructure.services.aiohttp.engine import engine


class NewsAdapter():
    def __init__(self, session: aiohttp.ClientSession, filters: NewsFilters):
        self._session = session
        self._filters = filters

    def get_filters(self):
        return self._filters

    async def _request(self, method: str, url: str, body: dict | None = None):
        try:
            async with self._session.request(
                method=method,
                url=url,
                headers={"X-Api-Key": config.news_api.API_KEY},
                data=body,
            ) as response:
                response_body = {}
                if response.status != HTTPStatus.NO_CONTENT:
                    response_body = await response.json()
            return response_body, response.status
        except Exception as e:
            raise NewsRepoError from e

    async def get_url(self, filter: BaseFilter | None) -> str:
        query_string = ""
        if filter:
            query_params = filter.model_dump(mode="json", exclude_none=True)
            query_string = urlencode(query_params) if query_params else ""

        base_url = config.news_api.BASE_API_URL
        url = f"{base_url}{filter.get_url_part() if filter else ''}?{query_string}"
        return url

    @staticmethod
    def parse_dict_to_filters(data: dict[str, Any]) -> BaseFilter:
        schemas = BaseFilter.__subclasses__()
        if not schemas:
            raise FilterSchemaNotFound

        for schema in schemas:
            try:
                parsed_model = schema.model_validate(data)
                return parsed_model
            except (ValidationError, TypeError):
                continue
        raise FilterSchemaNotFound

    async def get_news_list(self) -> Sequence[News]:
        if self._filters and not isinstance(self._filters, BaseFilter):
            raise NewsRepoError("Invalid filter format")
        response_news = None
        url = await self.get_url(self._filters)
        body, status = await self._request("GET", url)
        if status == HTTPStatus.OK:
            try:
                response_news = NewsResponse.model_validate(body)
            except ValidationError:
                raise NewsRepoError("Invalid news data format")
            return response_news.news
        print(url, body, status)
        raise NewsRepoError(f"Unexpected status code: {status}")


class TopHeadlinesNewsAdapter(NewsAdapter, NewsPort):
    @staticmethod
    async def create(filters_dict: dict[str, Any]) -> "NewsPort":
        filters = None
        try:
            filters = TopHeadlinesFilter.model_validate(filters_dict)
        except PydanticValidationError as e:
            for error in e.errors():
                raise ValidationError(error['msg'])
        if not isinstance(filters, TopHeadlinesFilter):
            raise NewsRepoError
        return TopHeadlinesNewsAdapter(await engine.get_session(), filters)


class EverythingNewsAdapter(NewsAdapter, NewsPort):
    @staticmethod
    async def create(filters_dict: dict[str, Any]) -> "NewsPort":
        filters = None
        try:
            filters = EverythingFilters.model_validate(filters_dict)
        except PydanticValidationError as e:
            for error in e.errors():
                raise ValidationError(error['msg'])
        if not isinstance(filters, EverythingFilters):
            raise ValidationError("wrong transmitted filters type")
        return EverythingNewsAdapter(await engine.get_session(), filters)
