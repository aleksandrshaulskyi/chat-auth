from application.exceptions import AuthenticationException
from application.ports import (
    DatabaseUnitOfWorkPort,
    DefaultHasherPort,
    JWTManagerPort,
    SessionRepositoryPort,
    UserRepositoryPort,
)
from domain.entities import Session


class CreateSessionUseCase:
    """
    This use case is responsible for the creation of sessions.
    """

    def __init__(
        self,
        session_data: dict,
        session_database_repo: SessionRepositoryPort,
        user_database_repo: UserRepositoryPort,
        default_hasher: DefaultHasherPort,
        jwt_manager: JWTManagerPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            session_data (dict): Raw data required to create a session.
            session_database_repo (SessionRepositoryPort): Repository for session persistence operations.
            user_database_repo (UserRepositoryPort): Repository for retrieving user authentication data.
            default_hasher (DefaultHasherPort): Password hashing and verification service.
            jwt_manager (JWTManagerPort): Service for generating JWT tokens.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work managing atomic database operations.
        """
        self.session_data = session_data
        self.session_database_repo = session_database_repo
        self.user_database_repo = user_database_repo
        self.default_hasher = default_hasher
        self.jwt_manager = jwt_manager
        self.database_uow = database_uow
        self.user_id = None

    async def execute(self) -> dict:
        await self.check_and_get_user_id()
        await self.get_and_terminate_sessions()

        session = await self.create_new_session()

        await self.database_uow.commit()

        return session.representation

    async def check_and_get_user_id(self) -> None:
        """
        Check authentication credentials and get a user id.

        If a user with provided data does exist set the use case property.

        Raises:
            AuthenticationException: The exception raisen should something go wrong while authentication.
        """
        username = self.session_data.get('username')
        password = self.session_data.get('password')

        exception_details = {
            'details': {
                'username': 'Authentication data is incorrect.',
                'password': 'Authentication data is incorrect.',
            }
        }

        if (user_data := await self.user_database_repo.get_by_properties({'username': username})) is not None:
            password_is_correct = await self.default_hasher.verify(value=password, hash=user_data.get('password'))

            if not password_is_correct:
                raise AuthenticationException(title='Authentication exception.', details=exception_details)

            self.user_id = user_data.get('id')

        else:
            raise AuthenticationException(title='Authentication exception.', details=exception_details)

    async def get_and_terminate_sessions(self) -> None:
        """
        Get all the sessions of a requesting user for the provided user-agent 
        that are not terminated and terminate them.
        """
        user_agent = self.session_data.get('user_agent')

        filters = {
            'user_id': self.user_id,
            'user_agent': user_agent,
            'terminated': False,
        }

        sessions_data = await self.session_database_repo.get_sessions(filters)

        if sessions_data:
            sessions = [Session(**session_data) for session_data in sessions_data]
            for session in sessions:
                session.terminate()
                await self.session_database_repo.update_session(session_id=session.id, data=session.representation)

    async def create_new_session(self) -> Session:
        """
        Create a new session.

        Issue a pair of access and refresh tokens, prepare session data and create an instance of Session.
        """
        token_pair = await self.jwt_manager.issue_pair(user_id=self.user_id)
        new_session_data = {'user_id': self.user_id, 'user_agent': self.session_data.get('user_agent'), **token_pair}
        created_session_data = await self.session_database_repo.create_session(data=new_session_data)

        session = Session(**created_session_data)

        return session
