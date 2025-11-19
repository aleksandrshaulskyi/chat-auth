from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from application.use_cases import TerminateSessionUseCase


class TerminateSessionController:
    """
    This controller is responsible for the termination of a session.
    """

    def __init__(
        self,
        user_id: int,
        user_agent: str,
        database_repo: SessionRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            user_id (int): The id of requesting user.
            user_agent (str): The user_agent.
            database_repo (SessionRepositoryPort): Repository handling session storage operations.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.user_id = user_id
        self.user_agent = user_agent
        self.database_repo = database_repo
        self.database_uow = database_uow

    def prepare_session_data(self) -> dict:
        """
        Prepare the required data for the termination of a session.

        Returns:
            dict: The data that is needed by the use case in order to terminate a session.
        """

        return {'user_id': self.user_id, 'user_agent': self.user_agent}

    async def terminate_session(self) -> None:
        """
        Terminate a session for a provided user agent.
        """
        use_case = TerminateSessionUseCase(
            session_data=self.prepare_session_data(),
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        await use_case.execute()
