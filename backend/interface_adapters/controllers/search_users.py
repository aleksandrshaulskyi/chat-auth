from application.ports import UserRepositoryPort
from application.use_cases import SearchUsersUseCase
from interface_adapters.outgoing_dtos import OutgoingUserDTO


class SearchUsersController:
    """
    This controller is responsible for the searching the users by their username.
    """

    def __init__(self, username: str, user: dict, database_repo: UserRepositoryPort) -> None:
        """
        Initialize the controller.

        Args:
            username (str): A username to be used as a search parameter.
            user (dict): A dictionary that represent the requesting user.
            database_repo (UserRepositoryPort): The port that is responsible for the actions with users.
        """
        self.username = username
        self.user = user
        self.database_repo = database_repo

    async def search_users(self) -> list:
        """
        Search users.
        """
        use_case = SearchUsersUseCase(
            username=self.username,
            user_username=self.user.get('username'),
            database_repo=self.database_repo,
        )

        return [OutgoingUserDTO.from_dict(user_data) for user_data in await use_case.execute()]
