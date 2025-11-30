from logging import getLogger

from settings import settings

from application.exceptions import SessionDoesNotExistException
from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from domain.entities import Session


class TerminateAllSessionsUseCase:
    """
    This use case terminates all the existing active user sessions.
    """

    def __init__(
        self,
        user_id: int,
        database_repo: SessionRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_id (int): Identifier of the user whose sessions should be terminated.
            database_repo (SessionRepositoryPort): Repository managing session persistence operations.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.user_id = user_id
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.logger = getLogger(settings.sessions_logger_name)

    async def execute(self) -> None:
        """
        Execute the process.

        - Get all the existing ongoing sessions of the requesting user.
        - Terminate them.
        """
        await self.database_repo.terminate_sessions(ids=await self.get_session_ids())
        await self.database_uow.commit()

    async def get_session_ids(self) -> set | None:
        """
        Get the ids of ongoing user sessions.

        Returns:
            set | None: The set of the ongoing user sessions.

        Raises:
            SessionDoesNotExistException: If no ongoing session exists.
        """
        filters = {
            'user_id': self.user_id,
            'terminated': False,
        }

        sessions_data = await self.database_repo.get_sessions(filters=filters)

        if sessions_data:
            return {session.get('id') for session in sessions_data}
        self.logger.error(
            'The user does not have any active sessions.',
            extra={'user_id': self.user_id, 'event_type': 'No active sessions of user.'},
        )
        raise SessionDoesNotExistException(
                title='Session does not exist.',
                details={'Session does not exist..': 'There is no active session for the user'},
            )
