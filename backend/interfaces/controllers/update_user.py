from dataclasses import asdict

from application.ports import DatabaseUnitOfWorkPort, UserRepositoryPort
from application.use_cases import UpdateUserUseCase
from domain.entities import User
from interfaces.dto.user_out import UserOut


class UpdateUserController:

    def __init__(self, user: User, user_data: dict, database_repo: UserRepositoryPort, database_uow: DatabaseUnitOfWorkPort) -> None:
        self.user = user
        self.user_data = user_data
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def update_user(self) -> UserOut:
        user_id = self.user.id

        self.user_data.update({'user_id': user_id})

        use_case = UpdateUserUseCase(
            user_data=self.user_data,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        user = await use_case.execute()

        return UserOut.from_dict(asdict(user))
