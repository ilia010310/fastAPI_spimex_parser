from typing import AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncConnection
)

from src.config import settings

async_engine = create_async_engine(
    url=settings.DB_URL,
    echo=True,
    future=True,
    pool_size=50,
    max_overflow=100,
    connect_args={
        'prepared_statement_name_func': lambda: f'__asyncpg_{uuid4()}__',
    }
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.begin() as conn:
        yield conn
