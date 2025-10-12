from settings import settings

from application.exceptions import DataIntegrityException, UserNotFoundException
from application.ports import DatabaseUnitOfWorkPort, FileStoragePort, UserRepositoryPort


class UpdateAvatarUseCase:

    def __init__(
        self,
        avatar: bytes,
        extension: str,
        user_id: int,
        file_storage: FileStoragePort,
        database_repo: UserRepositoryPort,
        database_uow: DatabaseUnitOfWorkPort,
    ) -> None:
        self.avatar = avatar
        self.extension = extension
        self.user_id = user_id
        self.file_storage = file_storage
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def execute(self) -> str | None:
        if self.extension not in settings.allowed_extensions:
            exception_details = {
                'details': {
                    'avatar': f'{self.extension} is not allowed. Use one of the following {settings.allowed_extensions}',
                    }
                }
            raise DataIntegrityException(details=exception_details)
        
        if len(self.avatar) > settings.max_size:
            exception_details = {
                'details': {
                    'avatar': f'Allowed file size is {settings.max_size} bytes and file exceeds limit.',
                    }
                }
            raise DataIntegrityException(details=exception_details)

        avatar_url = await self.file_storage.store(bfile=self.avatar, user_id=self.user_id, extension=self.extension)
        full_avatar_url = await self.make_full_avatar_url(avatar_url=avatar_url)

        try:
            await self.database_repo.update_avatar(avatar_url=full_avatar_url, user_id=self.user_id)
            await self.database_uow.commit()
        except UserNotFoundException:
            await self.file_storage.delete(path=full_avatar_url)
            exception_details = {'details': {'non-field-error': 'A user with the provided id does not exist.'}}
            raise DataIntegrityException(details=exception_details)
        else:
            return {'avatar_url': full_avatar_url}

    async def make_full_avatar_url(self, avatar_url: str) -> str:
        return f'{settings.current_domain}/{avatar_url}'
