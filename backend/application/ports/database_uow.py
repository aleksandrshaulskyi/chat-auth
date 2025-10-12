from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type


class DatabaseUnitOfWorkPort(ABC):

    @abstractmethod
    async def __aenter__(self) -> 'DatabaseUnitOfWorkPort':
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
