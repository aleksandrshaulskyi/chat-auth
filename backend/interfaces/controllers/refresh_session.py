from dataclasses import asdict

from application.ports import DatabaseUnitOfWorkPort, JWTTokenProviderPort, SessionRepositoryPort
from application.use_cases import RefreshSessionUseCase
from domain.entities import Session
from interfaces.dto import SessionOut


class RefreshSessionController:

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

    async def refresh_session(self) -> Session | None:
        use_case = RefreshSessionUseCase(
            session_data=self.session_data,
            session_database_repo=self.session_database_repo,
            jwt_provider=self.jwt_provider,
            database_uow=self.database_uow,
        )

        if (session := await use_case.execute()) is not None:
            return SessionOut.from_dict(asdict(session))
        return None
