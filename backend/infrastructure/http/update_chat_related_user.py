from asyncio import TimeoutError

from aiohttp import ClientConnectionError, ClientError, ClientSession
from backoff import expo, on_exception, full_jitter

from settings import settings

from application.exceptions import ChatsServerUnavailable
from application.ports import UpdateChatRelatedUserPort


class UpdateChatRelatedUser(UpdateChatRelatedUserPort):
    """
    The service that is responsible for the updating the information
    about users related to a chat when they update such information about themselves.
    """

    def __init__(self) -> None:
        """
        Initialize the service.
        """
        self.url = f'{settings.messaging_backend_url}/messaging/chats/update-chat-related-user'

    @on_exception(
        expo,
        (ClientError, TimeoutError),
        max_time=30,
        jitter=full_jitter,
    )
    async def execute(self, access_token: str, user_data: dict) -> bool:
        """
        Execute the update process.

        Request the endpoint. Retry for 30 seconds if request fails with the jitter.

        Returns:
            bool: True if received 204.

        Raises:
            ChatsServerUnavailable: Raisen if server did not respond or responded with 4xx or 5xx code.
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        try:
            async with ClientSession() as session:
                async with session.post(url=self.url, headers=headers, json=user_data) as response:
                    try:
                        response.raise_for_status()
                    except ClientError:
                        raise ChatsServerUnavailable(
                            title='Unprocessable response was returned.',
                            details={'Unprocessable response code.': 'Returned response with unprocessable code.'},
                        )
                    return True
        except (ClientConnectionError, TimeoutError):
            raise ChatsServerUnavailable(
                title='External server is unavailable.',
                details={'Connection error.': 'Could not connect to a server that returns required data.'},
            )
