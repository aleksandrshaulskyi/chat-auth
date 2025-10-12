from dataclasses import asdict

from application.exceptions import AuthenticationException, InvalidPasswordException, UserNotFoundException
from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, JWTTokenProviderPort, SessionRepositoryPort, UserRepositoryPort
from domain.entities import Session


class CreateSessionUseCase:

    def __init__(
        self,
        session_data: dict,
        session_database_repo: SessionRepositoryPort,
        user_database_repo: UserRepositoryPort,
        default_hasher: DefaultHasherPort,
        jwt_provider: JWTTokenProviderPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        self.session_data = session_data
        self.session_database_repo = session_database_repo
        self.user_database_repo = user_database_repo
        self.default_hasher = default_hasher
        self.jwt_provider = jwt_provider
        self.database_uow = database_uow
        self.user_id = None

    async def execute(self) -> Session:
        self.user_id = await self.check_and_get_user_id()
        await self.get_and_terminate_sessions()
        session = await self.create_new_session()
        await self.database_uow.commit()

        return session

    async def check_and_get_user_id(self) -> int | None:
        username = self.session_data.get('username')
        password = self.session_data.get('password')

        exception_details = {
            'details': {
                'username': 'Authentication data is incorrect.',
                'password': 'Authentication data is incorrect.',
            }
        }

        if (user_data := await self.user_database_repo.get_by_username(username=username)) is not None:
            try:
                await self.default_hasher.verify(value=password, hash=user_data.get('password'))
            except InvalidPasswordException:
                
                raise AuthenticationException(details=exception_details)
            else:
                return user_data.get('id')
        else:
            raise AuthenticationException(details=exception_details)
    
    async def get_and_terminate_sessions(self) -> None:
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
                await self.session_database_repo.update_session(session_id=session.id, data=asdict(session))

    async def create_new_session(self) -> Session:
        token_pair = await self.jwt_provider.issue_pair(user_id=self.user_id)
        new_session_data = {'user_id': self.user_id, 'user_agent': self.session_data.get('user_agent'), **token_pair}
        created_session_data = await self.session_database_repo.create_session(data=new_session_data)

        return Session(**created_session_data)
