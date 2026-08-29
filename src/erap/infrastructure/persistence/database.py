from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from erap.config.settings import get_settings


def create_engine() -> AsyncEngine:
    """Create the SQLAlchemy asynchronous database engine."""
    settings = get_settings()

    return create_async_engine(
        settings.database_url,
        pool_pre_ping=True,
    )


engine = create_engine()

session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for a unit of work."""
    async with session_factory() as session:
        yield session
