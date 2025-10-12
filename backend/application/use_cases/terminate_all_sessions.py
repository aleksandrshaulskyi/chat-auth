from dataclasses import asdict

from application.exceptions import DataIntegrityException
from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from domain.entities import Session


class TerminateAllSessionsUseCase:

    def __init__(
        self,
        user_id: int,
        database_repo: SessionRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        self.user_id = user_id
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def execute(self) -> None:
        sessions = await self.get_sessions()

        for session in sessions:
            session.terminate()

            await self.update_session(session=session)

        await self.database_uow.commit()

    async def get_sessions(self) -> list | None:
        filters = {
            'user_id': self.user_id,
        }

        sessions_data = await self.database_repo.get_sessions(filters=filters)

        if sessions_data:
            return [Session(**session_data) for session_data in sessions_data]
        exception_details = {'details': {'non-field-error': 'The user does not have any ongoing sessions at this moment.'}}
        raise DataIntegrityException(details=exception_details)
    
    async def update_session(self, session: Session) -> None:
        session_data = asdict(session)

        session_id = session_data.pop('id')

        await self.database_repo.update_session(session_id=session_id, data=session_data)
