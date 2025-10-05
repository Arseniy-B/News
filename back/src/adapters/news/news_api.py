from http import HTTPMethod, HTTPStatus
from typing import Any
from urllib.parse import urlencode

import aiohttp
from pydantic_settings import BaseSettings

from src.adapters.news.schemas.filter import BaseFilter, TopHeadlinesFilter
from src.adapters.news.schemas.news import NewsResponse
from src.config import config
from src.domain.exceptions import *
from src.domain.port.news_api import NewsClient


class AiohttpSessionEngine:
    def __init__(self) -> None:
        self.session: None | aiohttp.ClientSession = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self.session is None:
            connector = aiohttp.connector.TCPConnector(limit_per_host=100)
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self.session


engine = AiohttpSessionEngine()


class NewsAdapter(NewsClient):
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def _request(self, method: str, url: str, body: dict | None = None):
        try:
            print(url)
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
            raise NewsClientError from e

    async def get_url(self, filter: BaseFilter | None) -> str:
        query_string = ""
        if filter:
            query_params = {
                i: j for i, j in filter.model_dump(exclude_none=True).items() if i
            }
            query_string = urlencode(query_params) if query_params else ""
        url = config.news_api.BASE_API_URL + "top-headlines?" + query_string
        return url

    @staticmethod
    async def parse_dict_to_filters(data: dict[str, Any]) -> BaseFilter:
        schemas = BaseFilter.__subclasses__()
        if not schemas:
            raise

        for schema in schemas:
            try:
                parsed_model = schema.model_validate(**data)
                return parsed_model
            except ValidationError:
                continue
        raise

    async def get_news(self, filter: BaseFilter | None) -> NewsResponse:
        response_news = None
        url = await self.get_url(filter)
        body, status = await self._request("GET", url)
        if status == HTTPStatus.OK:
            try:
                response_news = NewsResponse.model_validate(body)
            except ValidationError:
                raise NewsFetchingError("Invalid news data format")
            return response_news
        raise NewsFetchingError(f"Unexpected status code: {status}")
