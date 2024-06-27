from typing import AsyncGenerator
import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.db.database import get_async_session, Base

from src.main import app
from src.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                        DB_USER_TEST)

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
REDIS_URL = "redis://localhost:6379"

engine_test = create_async_engine(
    url=DATABASE_URL_TEST,
    poolclass=NullPool,
    echo=True,
    pool_pre_ping=True,
)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    # Привязка метаданных к тестовому движку
    Base.metadata.bind = engine_test

    async with engine_test.begin() as conn:
        print("Подключение к тестовой базе данных")
        await conn.run_sync(Base.metadata.drop_all)
        print("Удалены все таблицы")
        await conn.run_sync(Base.metadata.create_all)
        print("Созданы все таблицы")

    yield

    # async with engine_test.begin() as conn:
    #     print("Удаление всех таблиц в конце тестов")
    #     await conn.run_sync(Base.metadata.drop_all)
    #     print("Все таблицы удалены")


# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


client = TestClient(app)
transport = ASGITransport(app=app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
