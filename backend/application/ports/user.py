from abc import ABC, abstractmethod

from domain.entities.user import User


class UserRepositoryPort(ABC):

    @abstractmethod
    async def create(self, user_data: dict) -> dict:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> dict | None:
        ...

    @abstractmethod
    async def get_by_id(self, id: int) -> dict | None:
        ...

    @abstractmethod
    async def update_user(self, user_id: int, user_data: dict) -> dict | None:
        ...

    @abstractmethod
    async def update_avatar(self, avatar_url: str) -> None:
        ...
