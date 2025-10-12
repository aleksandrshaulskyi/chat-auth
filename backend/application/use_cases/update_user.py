from application.exceptions import DataIntegrityException, UserNotFoundException
from application.ports import DatabaseUnitOfWorkPort, UserRepositoryPort
from domain.entities import User


class UpdateUserUseCase:

    def __init__(
        self,
        user_data: dict,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        self.user_data = user_data
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def execute(self) -> User | None:
        user_id = self.user_data.get('user_id')
        try:
            user_data = await self.database_repo.update_user(user_id=user_id, user_data=self.user_data)
        except UserNotFoundException as exception:
            constraint_field_name = await exception.get_constraint_field_name()
            exception_details = {'details': {constraint_field_name: f'A user with such {constraint_field_name} does already exist.'}}
            raise DataIntegrityException(details=exception_details)
        else:
            if user_data is not None:
                await self.database_uow.commit()
                return User(**user_data)
        exception_details = {'details': {'non-field-error': 'A user with the provided id does not exist.'}}
        raise DataIntegrityException(details=exception_details)
