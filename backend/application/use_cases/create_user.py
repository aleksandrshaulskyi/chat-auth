from application.exceptions import DataIntegrityException, UserAlreadyExistsException
from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, UserRepositoryPort
from domain.entities.user import User


class CreateUserUseCase:

    def __init__(
            self,
            user_data: dict,
            default_hasher: DefaultHasherPort,
            database_repo: UserRepositoryPort,
            database_uow: DatabaseUnitOfWorkPort,
        ) -> None:
        self.user_data = user_data
        self.default_hasher = default_hasher
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def execute(self) -> dict:
        raw_password = self.user_data.get('password')

        hashed_password = await self.default_hasher.hash(raw_password)

        user = User(**self.user_data)
        user.set_password(hashed_password=hashed_password)

        user_data = user.repr_without_none()

        try:
            user_model_dict = await self.database_repo.create(user_data=user_data)
        except UserAlreadyExistsException as exception:
            constraint_field_name = await exception.get_constraint_field_name()
            exception_details = {
                'details': {constraint_field_name: f'A user with such {constraint_field_name} has been already registered.'},
            }
            raise DataIntegrityException(details=exception_details)

        await self.database_uow.commit()

        return user_model_dict
