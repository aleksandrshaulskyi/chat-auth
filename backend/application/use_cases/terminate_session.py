from application.exceptions import SessionDoesNotExistException
from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from domain.entities import Session


class TerminateSessionUseCase:
    """
    This use case terminates a session for the provided user agent.
    """

    def __init__(
        self,
        session_data: dict,
        database_repo: SessionRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Args:
            session_data (dict): Raw data provided to create a session.
            database_repo (SessionRepositoryPort): Repository handling session storage operations.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.session_data = session_data
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.session = None

    async def execute(self) -> None:
        """
        Execute the process.

        - Get the session if any exist for such user and user agent.
        - Terminate the session.
        - Update it in the database.
        """
        await self.get_session()

        if self.session:
            self.session.terminate()

            await self.update_session()
            await self.database_uow.commit()

    async def get_session(self) -> None:
        """
        Get the session.

        Filter the existing sessions by the user id and user agent.
        If any is found set it as the use case property.

        Raises:
            SessionDoesNotExistException: Raisen if no session was foind for such user id and user agent.
        """
        user_id = self.session_data.get('user_id')
        user_agent = self.session_data.get('user_agent')

        filters = {
            'user_id': user_id,
            'user_agent': user_agent,
            'terminated': False,
        }

        if (session_data := await self.database_repo.get_session(filters=filters)) is not None:
            session = Session(**session_data)
            if session.is_ongoing:
                self.session = session
        else:
            raise SessionDoesNotExistException(
                    title='Session does not exist.',
                    details={'Session does not exist..': 'There is no active session for the user-agent.'},
                )

    async def update_session(self) -> None:
        """
        Update the terminated session in the database.
        """
        session_data = self.session.representation
        session_id = session_data.pop('id')

        await self.database_repo.update_session(session_id=session_id, data=session_data)
