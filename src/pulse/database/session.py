"""
Database session management for Pulse
Async SQLAlchemy session handling with SQLite
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..settings import settings
from .models import Base


# Global variables for engine and session factory
engine = None
async_session_factory = None


async def init_database() -> None:
    """Initialize database engine and create tables"""
    global engine, async_session_factory

    # Create async engine for SQLite
    engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,  # Log SQL queries in debug mode
        future=True,
    )

    # Create session factory
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_database() -> None:
    """Close database connections"""
    global engine
    if engine:
        await engine.dispose()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session with automatic cleanup

    Usage:
        async with get_async_session() as session:
            # Use session here
            pass
    """
    if async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get database session

    Usage in FastAPI endpoints:
        async def my_endpoint(session: AsyncSession = Depends(get_session)):
            # Use session here
            pass
    """
    async with get_async_session() as session:
        yield session
