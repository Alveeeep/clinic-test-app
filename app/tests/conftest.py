import pytest
from alembic.command import upgrade
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.db import Base, async_session_maker, engine
from app.dependencies.dao_dep import (
    get_session_with_commit,
    get_session_without_commit,
)
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DB_URL))
    upgrade(alembic_cfg, "head")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield await session.__aenter__()
            await session.rollback()  # Всегда откатываем после теста
        finally:
            await session.__aexit__(None, None, None)


@pytest.fixture
async def db_session_with_commit() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield await session.__aenter__()
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.__aexit__(None, None, None)


@pytest.fixture
async def db_session_without_commit() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield await session.__aenter__()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.__aexit__(None, None, None)


@pytest.fixture
async def client():
    # Создаем новую сессию для клиента
    session = async_session_maker()

    async def override_session_with_commit():
        try:
            yield await session.__aenter__()
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.__aexit__(None, None, None)

    async def override_session_without_commit():
        try:
            yield await session.__aenter__()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.__aexit__(None, None, None)

    app.dependency_overrides.update({
        get_session_with_commit: override_session_with_commit,
        get_session_without_commit: override_session_without_commit,
    })

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    await session.close()
