import unittest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.infrastructure.adapters.news.schemas.filter import (
    CountryCode,
    TopHeadlinesFilter,
)
from src.infrastructure.repository.users.users import UserCreate, UserRepository
from src.infrastructure.services.db.models import Base
from tests.config import test_db_config


class DatabaseTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = create_async_engine(test_db_config.DATABASE_URL, future=True)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.session = self.async_session()
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def asyncTearDown(self):
        async with self.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())
        await self.session.close()


class TestUserRepo(DatabaseTestCase):
    async def test_set_news_filter(self):
        self.user_repo = UserRepository(session=self.session)
        user = await self.user_repo.create(
            user_create=UserCreate("aa", "aaaaaa", "aa@gmail.com")
        )
        await self.user_repo.set_news_filters(
            TopHeadlinesFilter(country=CountryCode.US), user_id=user.id
        )
        print("ok")

    async def test_get_news_filter(self):
        self.user_repo = UserRepository(session=self.session)
        user = await self.user_repo.create(
            user_create=UserCreate("bb", "bbbbbb", "bb@gmail.com")
        )
        await self.user_repo.set_news_filters(
            TopHeadlinesFilter(country=CountryCode.US), user_id=user.id
        )
        filters = await self.user_repo.get_news_filters(user_id=user.id)
        print(filters)
