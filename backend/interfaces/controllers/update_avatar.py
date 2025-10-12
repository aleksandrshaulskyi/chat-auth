from pathlib import Path

from application.ports import DatabaseUnitOfWorkPort, FileStoragePort, UserRepositoryPort
from application.use_cases import UpdateAvatarUseCase


class UpdateAvatarController:

    def __init__(
            self,
            file: bytes,
            file_name: str,
            user_id: int,
            file_storage: FileStoragePort,
            database_repo: UserRepositoryPort,
            database_uow: DatabaseUnitOfWorkPort,
        ) -> None:
        self.file = file
        self.file_name = file_name
        self.user_id = user_id
        self.file_storage = file_storage
        self.database_repo = database_repo
        self.database_uow = database_uow

    async def update_avatar(self) -> str:
        full_name = Path(self.file_name or '').name
        extension = ''.join(Path(full_name).suffixes).lower()

        use_case = UpdateAvatarUseCase(
            avatar=self.file,
            extension=extension,
            user_id=self.user_id,
            file_storage=self.file_storage,
            database_repo=self.database_repo,
            database_uow=self.database_uow,
        )

        return await use_case.execute()
