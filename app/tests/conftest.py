import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.db import engine
from app.main import app


# Настройка сессий с явным управлением транзакциями
async_session_maker = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.rollback()


@pytest_asyncio.fixture
async def db_session_with_commit() -> AsyncSession:
    async with async_session_maker() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def prevent_parallel_transactions(db_session: AsyncSession):
    async with db_session.begin_nested() as transaction:
        yield
        await transaction.rollback()
