from types import TracebackType
from typing import Optional, Type

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.ports.database_uow import DatabaseUnitOfWorkPort


class DatabaseUnitOfWork(DatabaseUnitOfWorkPort):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self) -> 'DatabaseUnitOfWork':
        self.session = self.session_factory()
        return self
    
    async def __aexit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        try:
            if exception_type is not None:
                await self.session.rollback()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except (IntegrityError, SQLAlchemyError):
            await self.session.rollback()
            raise

    async def rollback(self) -> None:
        await self.session.rollback()
