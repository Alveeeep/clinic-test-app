import pytest
from alembic.command import upgrade
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
import pytest_asyncio
from app.config import settings
from app.database.db import Base, async_session_maker, engine
from app.dependencies.dao_dep import (
    get_session_with_commit,
    get_session_without_commit,
)
from app.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.DB_URL))
    upgrade(alembic_cfg, "head")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    session = await async_session_maker().__aenter__()
    try:
        yield await session.__aenter__()
        await session.rollback()  # Всегда откатываем после теста
    finally:
        await session.__aexit__(None, None, None)


@pytest_asyncio.fixture
async def db_session_with_commit() -> AsyncSession:
    session = await async_session_maker().__aenter__()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.__aexit__(None, None, None)


@pytest_asyncio.fixture
async def db_session_without_commit() -> AsyncSession:
    session = await async_session_maker().__aenter__()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.__aexit__(None, None, None)


@pytest_asyncio.fixture
async def client():
    # Создаем новую сессию для клиента
    session = async_session_maker()

    async def override_session_with_commit():
        s = await session.__aenter__()
        try:
            yield s
            await s.commit()
        except Exception:
            await s.rollback()
            raise
        finally:
            await s.__aexit__(None, None, None)

    async def override_session_without_commit():
        s = await session.__aenter__()
        try:
            yield s
            await s.rollback()
        except Exception:
            await s.rollback()
            raise
        finally:
            await s.__aexit__(None, None, None)

    app.dependency_overrides.update(
        {
            get_session_with_commit: override_session_with_commit,
            get_session_without_commit: override_session_without_commit,
        }
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    await session.close()
