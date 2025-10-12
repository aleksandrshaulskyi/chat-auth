from dataclasses import asdict

from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, JWTTokenProviderPort, SessionRepositoryPort, UserRepositoryPort
from application.use_cases import CreateSessionUseCase

from interfaces.dto import SessionOut


class CreateSessionController:

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

    async def create_session(self) -> SessionOut:
        use_case = CreateSessionUseCase(
            session_data=self.session_data,
            session_database_repo=self.session_database_repo,
            user_database_repo=self.user_database_repo,
            default_hasher=self.default_hasher,
            jwt_provider=self.jwt_provider,
            database_uow=self.database_uow,
        )

        session = await use_case.execute()

        return SessionOut.from_dict(asdict(session))
