from logging import getLogger

from settings import settings

from application.exceptions import UserAlreadyExistsException
from application.ports import DatabaseUnitOfWorkPort, DefaultHasherPort, UserRepositoryPort
from domain.entities.user import User


class CreateUserUseCase:
    """
    This use case is responsible for creating users.
    """

    def __init__(
        self,
        user_data: dict,
        default_hasher: DefaultHasherPort,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_data (dict): Raw data required to create a user.
            default_hasher (DefaultHasherPort): Service used for hashing user credentials.
            database_repo (UserRepositoryPort): Repository responsible for persisting user records.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database operations.
        """
        self.user_data = user_data
        self.default_hasher = default_hasher
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.logger = getLogger(settings.users_logger_name)

    async def get_and_hash_password(self) -> str:
        """
        Retrieve the inputed password from the user data and hash it.
        """
        return await self.default_hasher.hash(self.user_data.get('password'))
    
    async def validate(self) -> None:
        """
        Validates the incoming data.

        Raises:
            UserAlreadyExistsException: Raisen if a user with the provided data already exists.
        """
        username = self.user_data.get('username')

        if await self.database_repo.check_if_exists({'username': username}):
            self.logger.error(
                'An attempt to create a user with the existing username.',
                extra={'user_id': None, 'event_type': 'Existing username.'}
            )
            raise UserAlreadyExistsException(
                title='User already exists.',
                details={'username': 'A user with such username already exists.'},
            )
        
        email = self.user_data.get('email')
   
        if await self.database_repo.check_if_exists({'email': email}):
            self.logger.error(
                'An attempt to create a user with the existing email.',
                extra={'user_id': None, 'event_type': 'Existing email.'}
            )
            raise UserAlreadyExistsException(
                title='User already exists.',
                details={'email': 'A user with such email already exists.'},
            )

    async def execute(self) -> dict | None:
        """
        Create a user.

        - Validate the incoming data.
        - Create an instance of a User entity.
        - Set hashed password.
        - Create a User in database.

        Returns:
            dict: A representation of a User from the database if provided data is valid.
        """
        await self.validate()

        user = User.create(self.user_data)
        user.set_password(hashed_password=await self.get_and_hash_password())

        user_model_dict = await self.database_repo.create(user_data=user.representation)

        await self.database_uow.commit()

        return user_model_dict
