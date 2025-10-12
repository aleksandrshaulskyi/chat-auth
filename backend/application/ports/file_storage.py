from abc import ABC, abstractmethod


class FileStoragePort(ABC):

    @abstractmethod
    async def store(self, bfile: bytes, user_id: int, extension: str) -> str:
        ...

    @abstractmethod
    async def delete(self, path: str) -> None:
        ...
