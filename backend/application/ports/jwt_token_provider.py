from abc import ABC, abstractmethod
from datetime import timedelta


class JWTTokenProviderPort(ABC):

    @abstractmethod
    async def issue_pair(self) -> dict:
        ...

    @abstractmethod
    async def issue_token(self, expiration_time: timedelta) -> str:
        ...

    @abstractmethod
    async def verify(self, token: str) -> bool:
        ...

    @abstractmethod
    async def get_user_id(self, token: str) -> str:
        ...
