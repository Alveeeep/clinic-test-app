import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.db import engine, Base
from app.main import app


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session(async_engine):
    async_session_local = async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )
    async with async_session_local() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
