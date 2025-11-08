from src.domain.port.users import UserPort, AuthPort
from src.domain.port.news_api import NewsPort
from src.domain.entities.news import News, NewsFilters
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound
from typing import Sequence


async def set_user_filters(
    user_port: UserPort, auth_port: AuthPort, news_port: NewsPort
) -> NewsFilters:
    if not auth_port.is_authenticated:
        raise UserNotAuthorized
    filters = news_port.get_filters()
    user_id = auth_port.get_user_id()
    if not user_id:
        raise UserNotFound
    await user_port.set_news_filters(filters, user_id)
    return filters


async def get_user_filters(
    user_port: UserPort,
    auth_port: AuthPort,
    filter_type: type[NewsFilters] | None = None,
) -> Sequence[NewsFilters]:
    if not auth_port.is_authenticated:
        raise UserNotAuthorized
    user_id = auth_port.get_user_id()
    return await user_port.get_news_filters(user_id, filter_type=filter_type)
