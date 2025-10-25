from src.domain.port.users import UserPort, AuthPort
from src.domain.port.news_api import NewsPort
from src.domain.entities.news import News, NewsFilters
from src.use_cases.exceptions import UserNotAuthorized, UserNotFound


async def set_user_filters(
    user_port: UserPort, news_port: NewsPort, auth_port: AuthPort
) -> NewsFilters:
    if not auth_port.is_authenticated:
        raise UserNotAuthorized
    filters = news_port.get_filters()
    user_id = auth_port.get_user_id()
    if not user_id:
        raise UserNotFound
    await user_port.set_news_filters(filters, user_id)
    return filters


async def get_user_filters(user_port: UserPort, auth_port: AuthPort) -> NewsFilters:
    if not auth_port.is_authenticated:
        raise UserNotAuthorized

    user_id = auth_port.get_user_id()
    if not user_id:
        raise UserNotFound

    return await user_port.get_news_filters(user_id)

