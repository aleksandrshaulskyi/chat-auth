







from abc import ABC, abstractmethod


class UpdateChatRelatedUserPort(ABC):
    """
    This abstract port defines methods that will be needed to update the information
    about users related to the chats when such users update information about themselves.
    """

    @abstractmethod
    async def execute(self, access_token: str, user_data: dict) -> None:
        ...
