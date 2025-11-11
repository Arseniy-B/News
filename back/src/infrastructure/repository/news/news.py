from src.domain.entities.news import NewsFilter
from src.domain.port.news_api import NewsFilterPort
from src.infrastructure.adapters.news.schemas.filter import BaseFilter
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.infrastructure.services.db.models import NewsFilterModel


class NewsFilterError(Exception):
    """an error in the filter repository itself"""


class IncorrectSchema(Exception):
    """a scheme was transmitted that the port implementation cannot work with"""


class FilterNotFound(Exception):
    """filter cannot be found"""


class NewsFilterRepository(NewsFilterPort):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def get_filter_by_type(filter_type: str) -> type[BaseFilter]:
        for i in BaseFilter.__subclasses__():
            if hasattr(i, 'model_fields') and 'filter_type' in i.model_fields:
                default_value = i.model_fields['filter_type'].default
                if default_value == filter_type:
                    return i
        raise FilterNotFound

    async def save(self, user_id: int, news_filter: NewsFilter):
        if not isinstance(news_filter, BaseFilter):
            raise IncorrectSchema
        await self._session.execute(
            delete(NewsFilterModel).where(
                NewsFilterModel.user_id == user_id,
                NewsFilterModel.filter_type == news_filter.filter_type,
            )
        )
        data = news_filter.model_dump(exclude_unset=True, exclude_none=True)
        if "filter_type" in data:
            del data["filter_type"]
        new_filter = NewsFilterModel(user_id=user_id, data=data, filter_type=news_filter.filter_type)
        self._session.add(new_filter)
        await self._session.commit()

    async def get_by_type(
        self, user_id: int, filter_types: list[str]
    ) -> Sequence[NewsFilter]:
        stmt = select(NewsFilterModel).where(NewsFilterModel.user_id == user_id)
        stmt = stmt.where(NewsFilterModel.filter_type.in_(filter_types))
        result = await self._session.execute(stmt)
        res = result.scalars().all()
        if not res:
            raise FilterNotFound
        list_of_filters = []
        for i in res:
            news_filter = self.get_filter_by_type(i.filter_type).model_validate(i.data)
            list_of_filters.append(news_filter)
        return list_of_filters
