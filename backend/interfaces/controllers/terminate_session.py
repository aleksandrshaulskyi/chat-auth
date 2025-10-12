from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from application.use_cases import TerminateSessionUseCase


class TerminateSessionController:

    def __init__(self, session_data: dict, database_repo: SessionRepositoryPort, database_uow: DatabaseUnitOfWorkPort) -> None:
        self.session_data = session_data
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def terminate_session(self) -> None:
        use_case = TerminateSessionUseCase(
            session_data=self.session_data,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        await use_case.execute()
