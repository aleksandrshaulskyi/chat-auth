from application.ports import DatabaseUnitOfWorkPort, SessionRepositoryPort
from application.use_cases import TerminateAllSessionsUseCase


class TerminateAllSessionsController:

    def __init__(self, user_id: int, database_repo: SessionRepositoryPort, database_uow: DatabaseUnitOfWorkPort,) -> None:
        self.user_id = user_id
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def terminate_all_sessions(self) -> None:
        use_case = TerminateAllSessionsUseCase(
            user_id=self.user_id,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        await use_case.execute()
