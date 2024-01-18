import contextlib
from typing import Annotated, Any, AsyncIterator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.config.settings import get_database_settings
from src.domain.models import Base

settings = get_database_settings()

engine_url = f"postgresql+asyncpg://{settings.user}:{
    settings.password}@{settings.host}:{settings.port}/{settings.name}"

engine = create_async_engine(engine_url)
engine_sync = create_engine(f"postgresql+psycopg://{settings.user}:{
                            settings.password}@{settings.host}:{settings.port}/{settings.name}")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    engine_url, {"echo": True})


async def get_db():
    async with sessionmanager.session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()

        finally:
            await session.close()


# @contextlib.contextmanager
# def get_sync_db():
#     with engine_sync.begin() as con:
#         yield con


SessionDB = Annotated[AsyncSession, Depends(get_db)]
