from application.ports import UserRepositoryPort


class GetUsersInfoUseCase:
    """
    This use case is responsible for the retrieving information about specified users.
    """

    def __init__(self, user_ids: list, database_repo: UserRepositoryPort) -> None:
        """
        Initialize the use case.

        Args:
            user_ids (list): A list of user ids that specify the users to be found.
            database_repo (UserRepositoryPort): The port that is responsible for actions with users.
        """
        self.user_ids = user_ids
        self.database_repo = database_repo

    async def execute(self) -> list:
        """
        Find the specified users.
        """
        return await self.database_repo.get_by_ids(ids=self.user_ids)
