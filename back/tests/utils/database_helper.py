import unittest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
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
