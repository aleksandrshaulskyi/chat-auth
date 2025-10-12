from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, UserRepositoryPort
from application.use_cases import CreateUserUseCase
from interfaces.dto.user_out import UserOut


class CreateUserController:

    def __init__(
            self,
            user_data: dict,
            default_hasher: DefaultHasherPort,
            database_repo: UserRepositoryPort,
            database_uow: DatabaseUnitOfWorkPort
        ) -> None:
        self.user_data = user_data
        self.default_hasher = default_hasher
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def create_user(self) -> UserOut:
        use_case = CreateUserUseCase(
            user_data=self.user_data,
            default_hasher=self.default_hasher,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        user_data = await use_case.execute()

        return UserOut.from_dict(user_data)
