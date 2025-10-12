from os.path import join
from pathlib import Path
from time import time

from aiofiles import open as aioopen

from settings import settings

from application.ports import FileStoragePort


class FileStorage(FileStoragePort):

    def __init__(self) -> None:
        self.base_path = settings.display_media_root

    async def store(self, bfile: bytes, user_id: int, extension: str) -> str:
        file_name = f'{user_id}_{time()}{extension}'
        file_path = join(self.base_path, file_name)

        async with aioopen(file_path, 'wb') as file:
            await file.write(bfile)

        return file_path

    async def delete(self, path: str) -> None:
        Path(path).unlink(missing_ok=True)
