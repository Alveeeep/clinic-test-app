import asyncio
from pathlib import Path
from httpx import AsyncClient, ASGITransport
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import settings
from app.database.db import Base, engine
from app.dependencies.dao_dep import (
    get_session_with_commit,
    get_session_without_commit,
)
from app.main import app


# Настройка сессий с явным управлением транзакциями
async_session_maker = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def apply_migrations():
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DB_URL))

    async with engine.begin() as conn:
        await conn.run_sync(lambda c: command.upgrade(alembic_cfg, "head"))


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Очистка старых миграций
    migrations_dir = Path("alembic/versions")
    if migrations_dir.exists():
        for f in migrations_dir.glob("*.py"):
            f.unlink()

    # Применение миграций
    await apply_migrations()
    yield

    # Очистка после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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
    async def override_get_db():
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    yield session
                except Exception:
                    await session.rollback()
                    raise

    app.dependency_overrides.update(
        {
            get_session_with_commit: override_get_db,
            get_session_without_commit: override_get_db,
        }
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
