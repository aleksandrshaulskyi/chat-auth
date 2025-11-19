from application.ports import DatabaseUnitOfWorkPort, UpdateChatRelatedUserPort, UserRepositoryPort
from application.use_cases import UpdateUserUseCase
from interface_adapters.outgoing_dtos import OutgoingUserDTO


class UpdateUserController:
    """
    This controller is responsible for updating a user data.
    """

    def __init__(
        self,
        user_id: int,
        user_data: dict,
        access_token: str,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
        http_service: UpdateChatRelatedUserPort,
    ) -> None:
        """
        Initialize the controller.

        Args:
            user_id (int): The id of a user that will be updated.
            user_data (dict): Incoming data containing fields to update.
            access_token (str): The token required to perform a user identification.
            database_repo (UserRepositoryPort): Repository responsible for persisting user changes.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic update operations.
            http_service (UpdateChatRelatedUserPort): The port for the http service that updates chats.
        """
        self.user_id = user_id
        self.user_data = user_data
        self.access_token = access_token
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.http_service = http_service

    def prepare_data(self) -> None:
        """
        Prepares the data required by the use case.
        """
        self.user_data.update({'access_token': self.access_token, 'user_id': self.user_id})

    async def update_user(self) -> OutgoingUserDTO:
        """
        Update a user.

        Calls the respectful use case and returns the updated information in the
        approptiate format.
        """
        self.prepare_data()

        use_case = UpdateUserUseCase(
            user_data=self.user_data,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
            http_service=self.http_service,
        )

        return OutgoingUserDTO.from_dict(await use_case.execute())
