







from pathlib import Path

from application.ports import DatabaseUnitOfWorkPort, FileStoragePort, UserRepositoryPort, UpdateChatRelatedUserPort
from application.use_cases import UpdateAvatarUseCase


class UpdateAvatarController:
    """
    This controller is responsible for the updating the user avatar.
    """

    def __init__(
            self,
            file: bytes,
            file_name: str,
            user_id: int,
            access_token: str,
            file_storage: FileStoragePort,
            database_repo: UserRepositoryPort,
            database_uow: DatabaseUnitOfWorkPort,
            http_service: UpdateChatRelatedUserPort,
        ) -> None:
        """
        Initialize the controller.

        Args:
            file (bytes): Raw file content.
            file_name (str): Name of the uploaded file.
            user_id (int): ID of the user uploading the file.
            access_token (str): The token required to perform a user identification.
            file_storage (FileStoragePort): Port for file storage operations.
            database_repo (UserRepositoryPort): User repository port.
            database_uow (DatabaseUnitOfWorkPort): Unit of work for DB changes.
            http_service (UpdateChatRelatedUserPort): The port for the http service that updates chats.
        """
        self.file = file
        self.file_name = file_name
        self.user_id = user_id
        self.access_token = access_token
        self.file_storage = file_storage
        self.database_repo = database_repo
        self.database_uow = database_uow
        self.http_service = http_service

    def get_extension(self) -> str:
        """
        Get the extension of file.

        Returns:
            str: The file extension.
        """
        full_name = Path(self.file_name or '').name
        return ''.join(Path(full_name).suffixes).lower()

    async def update_avatar(self) -> str:
        """
        Update the user avatar.

        Returns:
            str: The path of the new user avatar.
        """
        use_case = UpdateAvatarUseCase(
            avatar=self.file,
            extension=self.get_extension(),
            user_id=self.user_id,
            access_token=self.access_token,
            file_storage=self.file_storage,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
            http_service=self.http_service,
        )

        return await use_case.execute()
