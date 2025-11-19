from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from application.use_cases import TerminateAllSessionsUseCase


class TerminateAllSessionsController:
    """
    This controller is responsible for the termination of all active user sessions.
    """

    def __init__(
        self,
        user_id: int,
        database_repo: SessionRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            user_id (int): Identifier of the user whose sessions should be terminated.
            database_repo (SessionRepositoryPort): Repository managing session persistence operations.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.user_id = user_id
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def terminate_all_sessions(self) -> None:
        """
        Call the use case.
        """
        use_case = TerminateAllSessionsUseCase(
            user_id=self.user_id,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        await use_case.execute()
