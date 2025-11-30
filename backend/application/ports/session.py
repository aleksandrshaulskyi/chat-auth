from abc import ABC, abstractmethod


class SessionRepositoryPort(ABC):

    @abstractmethod
    async def create_session(self, data: dict) -> dict:
        ...

    @abstractmethod
    async def get_session(self, filters: dict) -> dict | None:
        ...

    @abstractmethod
    async def get_sessions(self, user_id: int) -> list:
        ...

    @abstractmethod
    async def update_session(self, session_id: int, data: dict) -> dict | None:
        ...

    @abstractmethod
    async def terminate_sessions(self, ids: set) -> None:
        ...
