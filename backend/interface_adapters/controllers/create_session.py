from application.ports import (
    DatabaseUnitOfWorkPort,
    DefaultHasherPort,
    JWTManagerPort,
    SessionRepositoryPort,
    UserRepositoryPort,
)
from application.use_cases import CreateSessionUseCase

from interface_adapters.outgoing_dtos import OutgoingSessionDTO


class CreateSessionController:
    """
    This controller is responsible for creating sessions for users.
    """

    def __init__(
        self,
        session_data: dict,
        user_agent: str,
        session_database_repo: SessionRepositoryPort,
        user_database_repo: UserRepositoryPort,
        default_hasher: DefaultHasherPort,
        jwt_manager: JWTManagerPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            session_data (dict): Incoming raw session data from the transport layer.
            user_agent (str): The User-Agent string of the client creating the session.
            session_database_repo (SessionRepositoryPort): The port for session persistence.
            user_database_repo (UserRepositoryPort): The port for user persistence.
            default_hasher (DefaultHasherPort): The hasher used to verify user credentials.
            jwt_manager (JWTManagerPort): The JWT token provider.
            database_uow (DatabaseUnitOfWorkPort): The unit of work controlling the transaction.
        """
        self.session_data = session_data
        self.user_agent = user_agent
        self.session_database_repo = session_database_repo
        self.user_database_repo = user_database_repo
        self.default_hasher = default_hasher
        self.jwt_manager = jwt_manager
        self.database_uow = database_uow

    def prepare_create_session_data(self) -> dict:
        """
        Prepare and enrich the incoming session data.

        Returns:
            dict: The data that is required to create a session.
        """
        session_data = self.session_data
        session_data.update({'user_agent': self.user_agent})

        return session_data

    async def create_session(self) -> OutgoingSessionDTO:
        """
        Create a session.

        Call the respectful use case and return the data in the appropriate format.
        """
        use_case = CreateSessionUseCase(
            session_data=self.prepare_create_session_data(),
            session_database_repo=self.session_database_repo,
            user_database_repo=self.user_database_repo,
            default_hasher=self.default_hasher,
            jwt_manager=self.jwt_manager,
            database_uow=self.database_uow,
        )

        return OutgoingSessionDTO.from_dict(await use_case.execute())
