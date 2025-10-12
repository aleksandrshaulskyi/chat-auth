from dataclasses import asdict

from application.exceptions import AuthenticationException
from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from domain.entities import Session


class TerminateSessionUseCase:

    def __init__(self, session_data: dict, database_repo: SessionRepositoryPort, database_uow: DatabaseUnitOfWorkPort) -> None:
        self.session_data = session_data
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.session = None

    async def execute(self) -> None:
        self.session = await self.get_session()
        self.session.terminate()

        await self.update_session()
        await self.database_uow.commit()

    async def get_session(self) -> Session:
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
                return session
        raise AuthenticationException({'non-field-error': 'There is no active session for the provided token.'})
    
    async def update_session(self) -> None:
        session_data = asdict(self.session)

        session_id = session_data.pop('id')

        await self.database_repo.update_session(session_id=session_id, data=session_data)
