from logging import getLogger

from settings import settings

from application.exceptions import AuthenticationException
from application.ports import DatabaseUnitOfWorkPort, JWTManagerPort, SessionRepositoryPort
from domain.entities import Session


class RefreshSessionUseCase:
    """
    This use case is responsible for refreshing the sessions.
    """

    def __init__(
        self,
        session_data: dict,
        session_database_repo: SessionRepositoryPort,
        jwt_manager: JWTManagerPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            session_data (dict): Raw data required to create a session.
            session_database_repo (SessionRepositoryPort): Repository responsible for session persistence.
            jwt_manager (JWTManagerPort): Service used to issue JWT tokens.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work managing atomic database operations.
        """
        self.session_data = session_data
        self.session_database_repo = session_database_repo
        self.jwt_manager = jwt_manager
        self.database_uow = database_uow
        self.session = None
        self.user_id = None
        self.logger = getLogger(settings.sessions_logger_name)

    async def execute(self) -> dict | None:
        """
        Execute the process.

        - Set a user id.
        - Get the session with the provided user agent and refresh token.
        - Depending on session state prolong or terminate it.
        - Update the sesssion in database.

        Returns:
            dict: The representation of a session.

        Raises:
            AuthenticationException: Raisen if the provided token has already expired.
        """
        await self.set_user_id()
        await self.get_session()
        await self.prolong_or_terminate_session()
        await self.update_session()
        await self.database_uow.commit()

        if not self.session.terminated:
            return self.session.representation
        
        self.logger.error(
            'An attempt to refresh session with the expired refresh token.',
            extra={'user_id': self.user_id, 'event_type': 'Expired refresh token.'},
        )
        raise AuthenticationException(
            title='Authentication exception.',
            details={'Authentication exception.': 'The provided refresh token expired.'},
        )

    async def set_user_id(self) -> None:
        """
        Set the user id property with the ID that should be retrieved from the provided token.
        """
        self.user_id = await self.jwt_manager.get_user_id(token=self.session_data.get('refresh_token'))

    async def get_session(self) -> None:
        """
        Retrieve the session from the database based on user_agent and refresh_token and set it as the property.

        Raises:
            AuthenticationException: Raisen if no session was found with the provided values.
        """
        user_agent = self.session_data.get('user_agent')
        refresh_token = self.session_data.get('refresh_token')

        filters = {
            'user_id': self.user_id,
            'user_agent': user_agent,
            'refresh_token': refresh_token,
            'terminated': False,
        }

        if (session_data := await self.session_database_repo.get_session(filters=filters)) is not None:
            self.session = Session(**session_data)
        else:
            self.logger.error(
                'A session with the provided refresh token does not exist.',
                extra={'user_id': self.user_id, 'event_type': 'Session does not exist.'},
            )
            raise AuthenticationException(
                title='Authentication exception.',
                details={'Authentication exception.': 'No active session found for such refresh token.'},
            )
    
    async def prolong_or_terminate_session(self) -> None:
        """
        Prolong or terminate session base on its expiration time.

        A session gets prolonged if it is an ongoing session
        (i.e. it's valid through property is bigger than current time)
        and terminated otherwise.
        """
        if self.session.is_ongoing:
            token_pair = await self.jwt_manager.issue_pair(user_id=self.user_id)

            self.session.prolong(
                access_token=token_pair.get('access_token'),
                refresh_token=token_pair.get('refresh_token')
            )

        else:
            self.session.terminate()

    async def update_session(self) -> None:
        """
        Update the session in database.
        """
        updated_session_data = self.session.representation
        session_id = updated_session_data.pop('id')

        self.session = Session(
            **await self.session_database_repo.update_session(session_id=session_id, data=updated_session_data)
        )
