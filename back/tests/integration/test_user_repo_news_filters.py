from src.infrastructure.adapters.news.schemas.filter import (
    CountryCode,
    TopHeadlinesFilter,
)
from src.infrastructure.repository.users.users import UserRepository
from src.infrastructure.repository.users.schemas import UserCreate
from tests.utils.database_helper import DatabaseTestCase


class TestUserRepo(DatabaseTestCase):
    async def test_news_filters(self):
        self.user_repo = UserRepository(session=self.session)
        user = await self.user_repo.create(
            user_create=UserCreate(username="aa", password="aaaaaa", email="aa@gmail.com")
        )

        start_filters = TopHeadlinesFilter(country=CountryCode.US)
        await self.user_repo.set_news_filters(start_filters, user_id=user.id)

        finish_filters = await self.user_repo.get_news_filters(
            user_id=user.id, filter_type=TopHeadlinesFilter
        )

        self.assertEqual(start_filters, finish_filters[0])
