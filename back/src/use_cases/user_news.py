from src.domain.port.users import UserPort, AuthPort
from src.domain.port.news_api import NewsApiPort, NewsFilterPort
from src.domain.entities.news import News, NewsFilter
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound
from typing import Sequence


async def set_user_filter(
    auth_port: AuthPort,
    news_filter: NewsFilter,
    filter_port: NewsFilterPort,
):
    if not auth_port.is_authenticated:
        raise UserNotAuthorized
    user_id = auth_port.get_user_id()
    if not user_id:
        raise UserNotFound
    await filter_port.save(user_id, news_filter=news_filter)


async def get_user_filter(
    auth_port: AuthPort,
    filter_port: NewsFilterPort,
    filter_types: list[str],
) -> Sequence[NewsFilter]:
    if not auth_port.is_authenticated:
        raise UserNotAuthorized
    user_id = auth_port.get_user_id()
    return await filter_port.get_by_type(user_id, filter_types)
