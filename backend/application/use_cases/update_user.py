from logging import getLogger

from settings import settings

from application.exceptions import UserAlreadyExistsException, UserNotFoundException
from application.outgoing_dtos import OutgoingUserDTO
from application.ports import DatabaseUnitOfWorkPort, UpdateChatRelatedUserPort, UserRepositoryPort


class UpdateUserUseCase:
    """
    This use case is responsible for the updating the information
    about a user.
    """

    def __init__(
        self,
        user_data: dict,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
        http_service: UpdateChatRelatedUserPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            user_data (dict): Raw data required to create a new user.
            database_repo (UserRepositoryPort): Repository responsible for storing user records.
            database_uow (DatabaseUnitOfWorkPort): Unit of Work ensuring atomic database operations.
            http_service (UpdateChatRelatedUserPort): The port for the http service that updates chats.
        """
        self.user_data = user_data
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.http_service = http_service
        self.logger = getLogger(settings.users_logger_name)

    async def validate(self) -> None:
        """
        Validate the incoming data.

        Check if a user with the provided username or email already exist.

        Raises:
            UserAlreadyExistsException: Raisen if a user with the provided data already exist.
        """
        if (username := self.user_data.get('username')) is not None:
            self.logger.error(
                'An attempt to update a user info with the existing username.',
                extra={'user_id': self.user_id, 'event_type': 'Update user with existing username.'}
            )
            if await self.database_repo.check_if_exists({'username': username}):
                raise UserAlreadyExistsException(
                    title='User already exists.',
                    details={'username': 'A user with such username already exists.'},
                )
            
        if (email := self.user_data.get('email')) is not None:
            if await self.database_repo.check_if_exists({'email': email}):
                self.logger.error(
                    'An attempt to update a user info with the existing email.',
                    extra={'user_id': self.user_id, 'event_type': 'Update user with existing email.'}
                )
                raise UserAlreadyExistsException(
                    title='User already exists.',
                    details={'email': 'A user with such email already exists.'},
                )

    async def execute(self) -> dict | None:
        """
        Execute the process.

        - Validate the incoming data.
        - Update the information.
        """
        await self.validate()

        access_token = self.user_data.pop('access_token')

        user_data = await self.database_repo.update_user(
            user_id=self.user_data.get('user_id'),
            user_data=self.user_data,
        )

        outgoing_user = OutgoingUserDTO.create(user_data=user_data)

        if user_data is not None:
            if await self.http_service.execute(access_token=access_token, user_data=outgoing_user.representation):
                await self.database_uow.commit()
                return user_data

        self.logger.error(
            'A user with the provided id was not found.',
            extra={'user_id': self.user_id, 'event_type': 'Invalid user during the user info update.'}
        )

        raise UserNotFoundException(
            title='User was not found.',
            details={'User was not found.': 'A user with the provided id does not exist.'}
        )
