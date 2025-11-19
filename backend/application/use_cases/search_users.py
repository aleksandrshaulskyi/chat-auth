from application.ports import UserRepositoryPort


class SearchUsersUseCase:
    """
    The use case that is responsible for searching the users that match the provided username.
    """

    def __init__(self, username: str, user_username: str, database_repo: UserRepositoryPort) -> None:
        """
        Initialize the use case.

        Args:
            username (str): A username to be used as a search parameter.
            user_username (str): The username that specifies the user to be excluded from the search results.
            database_repo (UserRepositoryPort): The port that is responsible for the actions with users.
        """
        self.username = username
        self.user_username = user_username
        self.database_repo = database_repo

    async def execute(self) -> list:
        """
        Execute the process.
        """
        users = await self.database_repo.search_users_by_username(
            username=self.username,
            user_username=self.user_username,
        )
        return users
