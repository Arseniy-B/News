import unittest
from unittest.mock import AsyncMock, MagicMock, Mock

from src.infrastructure.adapters.news.schemas.filter import (
    CountryCode,
    TopHeadlinesFilter,
)
from src.infrastructure.repository.users.users import UserRepository


class TestUserRepo(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self): ...

    async def asyncTearDown(self): ...

    async def test_get_filters(self):
        class Ans():
            data = {"country": "US"}

        mock_data = Mock()
        mock_data.all.return_value = [Ans()]

        mock_scalars = Mock()
        mock_scalars.scalars.return_value = mock_data

        mock_session = AsyncMock()
        mock_session.execute.return_value = mock_scalars

        repo = UserRepository(session=mock_session)

        answer_filter = await repo.get_news_filters(
            user_id=1, filter_type=TopHeadlinesFilter
        )
        self.assertEqual(answer_filter[0], TopHeadlinesFilter(country=CountryCode.US))


    async def test_set_filters(self):
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock()
        mock_session.execute.return_value = "{}"
        mock_session.add = MagicMock()

        repo = UserRepository(session=mock_session)

        await repo.set_news_filters(
            TopHeadlinesFilter(country=CountryCode.US), user_id=1
        )
