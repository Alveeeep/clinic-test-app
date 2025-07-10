import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

from app.config import settings
from app.database.db import Base, async_session_maker, engine  # noqa
from app.dependencies.dao_dep import (
    get_session_with_commit,
    get_session_without_commit,
)
from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def run_async_migrations():
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DB_URL))

    # Создаем новую ревизию
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda conn: command.revision(
                config=alembic_cfg, autogenerate=True, message="test_migration"
            )
        )
    print("Миграция Создана")
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: command.upgrade(alembic_cfg, "head"))


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    migrations_dir = Path("alembic/versions")
    if migrations_dir.exists():
        for f in migrations_dir.glob("*.py"):
            f.unlink()

    # Запускаем миграции
    await run_async_migrations()

    yield

    # Очистка после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(
            lambda conn: conn.execute("DROP TABLE IF EXISTS alembic_version")
        )


@pytest_asyncio.fixture
async def db_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


@pytest_asyncio.fixture
async def db_session_with_commit():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
def client():
    async def override_get_db():
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides.update(
        {
            get_session_with_commit: override_get_db,
            get_session_without_commit: override_get_db,
        }
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
