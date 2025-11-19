from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, UserRepositoryPort
from application.use_cases import CreateUserUseCase
from interface_adapters.outgoing_dtos import OutgoingUserDTO


class CreateUserController:
    """
    The controller that is responsible for creating a user.

    It accepts the incoming data, transmits it to the use case
    and returns the adapted data.
    """

    def __init__(
            self,
            user_data: dict,
            default_hasher: DefaultHasherPort,
            database_repo: UserRepositoryPort,
            database_uow: DatabaseUnitOfWorkPort
        ) -> None:
        """
        Initialize the controller.

        Args:
            user_data (dict): Raw data required to create a new user.
            default_hasher (DefaultHasherPort): Service responsible for hashing sensitive fields.
            database_repo (UserRepositoryPort): Repository handling user persistence operations.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database actions.
        """
        self.user_data = user_data
        self.default_hasher = default_hasher
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def create_user(self) -> OutgoingUserDTO:
        """
        Create a user.

        Call the respectful use case and return adapted data.

        Returns:
            OutgoingUserDTO: The dataclass used to return an instance of User in the suitable
            representation.
        """
        use_case = CreateUserUseCase(
            user_data=self.user_data,
            default_hasher=self.default_hasher,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        return OutgoingUserDTO.from_dict(await use_case.execute())
