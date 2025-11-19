from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):

    @abstractmethod
    async def create(self, user_data: dict) -> dict:
        ...

    @abstractmethod
    async def check_if_exists(self, properties: dict) -> bool:
        ...

    @abstractmethod
    async def get_by_properties(self, properties: dict) -> dict | None:
        ...

    @abstractmethod
    async def get_by_ids(self, ids: list) -> list:
        ...

    @abstractmethod
    async def update_user(self, user_id: int, user_data: dict) -> dict | None:
        ...

    @abstractmethod
    async def update_avatar(self, avatar_url: str) -> None:
        ...

    @abstractmethod
    async def search_users_by_username(self, username: str, user_username: str) -> list:
        ...
