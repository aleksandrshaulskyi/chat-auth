from logging import getLogger

from settings import settings

from application.exceptions import FileExtensionException, FileSizeException, UserNotFoundException
from application.outgoing_dtos import OutgoingUserDTO
from application.ports import DatabaseUnitOfWorkPort, FileStoragePort, UpdateChatRelatedUserPort, UserRepositoryPort


class UpdateAvatarUseCase:
    """
    This use case is responsible for the update of a user avatar.
    """

    def __init__(
        self,
        avatar: bytes,
        extension: str,
        user_id: int,
        access_token: str,
        file_storage: FileStoragePort,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
        http_service: UpdateChatRelatedUserPort,
    ) -> None:
        """
        Initialize the use case.

        Args:
            avatar (bytes): Avatar file bytes.
            extension (str): File extension.
            user_id (int): User ID.
            access_token (str): The token required to identify the user.
            file_storage (FileStoragePort): File storage port.
            database_repo (UserRepositoryPort): User repository port.
            database_uow (DatabaseUnitOfWorkPort): Database unit of work.
            http_service (UpdateChatRelatedUserPort): The port for the http service that updates chats.
        """
        self.avatar = avatar
        self.extension = extension
        self.user_id = user_id
        self.access_token = access_token
        self.file_storage = file_storage
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.http_service = http_service
        self.logger = getLogger(settings.users_logger_name)

    def validate(self) -> None:
        """
        Validate the incoming data.

        Raises:
            FileExtensionException: If the file's extension is not supported.
            FileSizeException: If the file's size exceeds the limit.
        """
        if self.extension not in settings.allowed_extensions:
            self.logger.error(
                'An attempt to upload file with the wrong extension.',
                extra={'user_id': self.user_id, 'event_type': 'Wrong extension.'}
            )
            raise FileExtensionException(
                title='File extension exception.',
                details={'File extension exception.': 'This extension is not supported.'},
            )
        
        if len(self.avatar) > settings.max_size:
            self.logger.error(
                'An attempt to upload a file that is too large.',
                extra={'user_id': self.user_id, 'event_type': 'File is too large.'}
            )
            raise FileSizeException(
                title='File size exception.',
                details={'File size exception.': 'The file size exceeded the allowed file size.'},
            )
        
    async def store_file(self) -> str:
        """
        Store avatar in the local file storage and get it's full path.

        Returns:
            str: The full path of avatar.
        """
        avatar_url = await self.file_storage.store(bfile=self.avatar, user_id=self.user_id, extension=self.extension)
        return f'{settings.current_domain}/{avatar_url}'

    async def execute(self) -> str | None:
        """"
        Execute the process.

        - Validate the incoming data.
        - Store file in the storage.
        - Update avatar in the database.
        - Update user info in the messaging service.
        """
        self.validate()

        full_avatar_url = await self.store_file()

        user_data = await self.database_repo.update_avatar(avatar_url=full_avatar_url, user_id=self.user_id)

        outgoing_user = OutgoingUserDTO.create(user_data=user_data)

        if user_data is not None:
            if await self.http_service.execute(access_token=self.access_token, user_data=outgoing_user.representation):
                await self.database_uow.commit()
                return {'avatar_url': full_avatar_url}
        await self.file_storage.delete(path=full_avatar_url)
        self.logger.error(
            'A user with the provided id was not found.',
            extra={'user_id': self.user_id, 'event_type': 'Invalid user during avatar update.'}
        )
        raise UserNotFoundException(
            title='User was not found.',
            details={'User was not found.': 'A user matching the provided id does not exist.'},
        )
