import pytest
from alembic.command import upgrade
from alembic.config import Config
from fastapi.testclient import TestClient

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
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.TEST_DB_URL))
    upgrade(alembic_cfg, "head")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.rollback()  # Всегда откатываем после теста
        finally:
            await session.close()


@pytest.fixture
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
def client(db_session):
    # Переопределяем зависимости
    app.dependency_overrides[get_session_without_commit] = db_session
    app.dependency_overrides[get_session_with_commit] = db_session

    with TestClient(app) as test_client:
        yield test_client

    # Очищаем переопределения
    app.dependency_overrides = {}
