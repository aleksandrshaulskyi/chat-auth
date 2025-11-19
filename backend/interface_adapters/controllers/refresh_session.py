from application.ports import DatabaseUnitOfWorkPort, JWTManagerPort, SessionRepositoryPort
from application.use_cases import RefreshSessionUseCase
from interface_adapters.outgoing_dtos import OutgoingSessionDTO


class RefreshSessionController:
    """
    This controller is responsible for the process of sessions refreshing.
    """

    def __init__(
        self,
        session_data: dict,
        user_agent: str,
        session_database_repo: SessionRepositoryPort,
        jwt_manager: JWTManagerPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            session_data (dict): Raw data required to create a user session.
            user_agent (str): User-Agent string of the requesting client.
            session_database_repo (SessionRepositoryPort): Repository handling session storage operations.
            jwt_manager (JWTManagerPort): Service responsible for generating JWT tokens.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.session_data = session_data
        self.user_agent = user_agent
        self.session_database_repo = session_database_repo
        self.jwt_manager = jwt_manager
        self.database_uow = database_uow

    def prepare_session_data(self) -> dict:
        """
        Prepares the data that is required to refresh a session.

        Returns:
            dict: The data that is required by the use case to refresh a session.
        """
        session_data = self.session_data
        session_data.update({'user_agent': self.user_agent})

        return session_data

    async def refresh_session(self) -> OutgoingSessionDTO:
        """
        Refresh a session.

        Call the respectful use case and return the session data in the appropriate format.

        Returns:
            OutgoingSessionDTO: The dataclass representing a session.
        """
        use_case = RefreshSessionUseCase(
            session_data=self.prepare_session_data(),
            session_database_repo=self.session_database_repo,
            jwt_manager=self.jwt_manager,
            database_uow=self.database_uow,
        )

        return OutgoingSessionDTO.from_dict(await use_case.execute())
