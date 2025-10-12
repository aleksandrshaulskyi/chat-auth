from dataclasses import asdict

from application.exceptions import AuthenticationException, InvalidJWTException
from application.ports import DatabaseUnitOfWorkPort, JWTTokenProviderPort, SessionRepositoryPort
from domain.entities import Session


class RefreshSessionUseCase:

    def __init__(
        self,
        session_data: dict,
        session_database_repo: SessionRepositoryPort,
        jwt_provider: JWTTokenProviderPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        self.session_data = session_data
        self.session_database_repo = session_database_repo
        self.jwt_provider = jwt_provider
        self.database_uow = database_uow
        self.session = None
        self.user_id = None

    async def execute(self) -> Session | None:
        await self.set_user_id()
        self.session = await self.get_session()

        await self.prolong_or_terminate_session()

        await self.update_session()

        await self.database_uow.commit()

        return self.session

    async def set_user_id(self) -> None:
        try:
            self.user_id = await self.jwt_provider.get_user_id(token=self.session_data.get('refresh_token'))
        except InvalidJWTException:
            raise AuthenticationException(details={'non-field-error': 'Invalid JWT was provided.'})

    async def get_session(self) -> Session | None:
        user_agent = self.session_data.get('user_agent')
        refresh_token = self.session_data.get('refresh_token')

        filters = {
            'user_id': self.user_id,
            'user_agent': user_agent,
            'refresh_token': refresh_token,
            'terminated': False,
        }

        if (session_data := await self.session_database_repo.get_session(filters=filters)) is not None:
            return Session(**session_data)
        raise AuthenticationException({'non-field-error': 'There is no active session for the provided token.'})
    
    async def prolong_or_terminate_session(self) -> None:
        if self.session.is_ongoing:
            token_pair = await self.jwt_provider.issue_pair(user_id=self.user_id)

            self.session.prolong(
                access_token=token_pair.get('access_token'),
                refresh_token=token_pair.get('refresh_token')
            )

        else:
            self.session.terminate()

    async def update_session(self) -> Session:
        updated_session_data = asdict(self.session)
        session_id = updated_session_data.pop('id')

        self.session = Session(
            **await self.session_database_repo.update_session(session_id=session_id, data=updated_session_data)
        )
