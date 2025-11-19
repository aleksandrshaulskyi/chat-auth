from application.exceptions import UserNotFoundException
from application.ports import JWTManagerPort, UserRepositoryPort


class GetUserUseCase:
    """
    This use case is responsible for the retrieval of the requesting user.
    """

    def __init__(
        self,
        user_id: int,
        database_repo: UserRepositoryPort,
        jwt_manager: JWTManagerPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): The id of requesting user.
            database_repo (UserRepositoryPort): Repository responsible for persisting the users records.
            jwt_manager (JWTManagerPort): Service for generating JWT tokens.
        """
        self.user_id = user_id
        self.database_repo = database_repo
        self.jwt_manager = jwt_manager

    async def execute(self) -> dict | None:
        """
        Execute the process.

        Returns:
            dict | None: Returns a dictionary that represents the user
        """
        if (user_data := await self.database_repo.get_by_properties({'id': self.user_id})) is not None:
            return user_data
        raise UserNotFoundException(
            title='User was not found.',
            details={'User was not found.': 'A user matching provided data does not exist.'}
        )
