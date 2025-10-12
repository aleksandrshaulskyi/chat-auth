from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from settings import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.database_url,
        echo=settings.echo,
        pool_pre_ping=True,
        future=True,
    )

def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
