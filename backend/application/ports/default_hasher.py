from abc import ABC, abstractmethod


class DefaultHasherPort(ABC):

    @abstractmethod
    async def hash(self, value: str | int) -> str:
        ...

    @abstractmethod
    async def verify(self, value: str | int, hash: str | int) -> bool:
        ...
