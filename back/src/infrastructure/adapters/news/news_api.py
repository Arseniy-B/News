from http import HTTPStatus
from urllib.parse import urlencode

import aiohttp

from src.config import config
from src.domain.entities.news import (
    NewsResponse as DomainNewsResponse,
)
from src.domain.port.news_api import NewsApiPort, NewsFilter
from src.infrastructure.adapters.news.schemas.filter import (
    BaseFilter,
)
from src.infrastructure.adapters.news.schemas.news import NewsResponse
from src.infrastructure.exceptions import (
    NewsRepoError,
    ValidationError,
)


class NewsAdapter(NewsApiPort):
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

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
            raise NewsRepoError

    async def get_url(self, news_filter: BaseFilter) -> str:
        query_string = ""
        if news_filter:
            query_params = news_filter.model_dump_url(mode="json", exclude_none=True)
            query_string = urlencode(query_params) if query_params else ""

        base_url = config.news_api.BASE_API_URL
        url = f"{base_url}{news_filter.get_url_part() if filter else ''}?{query_string}"
        return url

    async def get_news_list(
        self, news_filter: NewsFilter
    ) -> DomainNewsResponse:
        if not isinstance(news_filter, BaseFilter):
            raise NewsRepoError("Invalid filter format")
        response_news = None
        url = await self.get_url(news_filter)
        body, status = await self._request("GET", url)
        if status == HTTPStatus.OK:
            try:
                response_news = NewsResponse.model_validate(body)
            except ValidationError:
                raise NewsRepoError("Invalid news data format")
            return response_news
        print(body, status)
        raise NewsRepoError(f"Unexpected status code: {status}")
