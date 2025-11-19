from os.path import join
from pathlib import Path
from time import time

from aiofiles import open as aioopen

from settings import settings

from application.ports import FileStoragePort


class FileStorage(FileStoragePort):
    """
    Store and delete files on the local filesystem.
    """

    def __init__(self) -> None:
        """
        Initialize the storage.
        """
        self.base_path = settings.display_media_root

    async def store(self, bfile: bytes, user_id: int, extension: str) -> str:
        """Save a file and return its filesystem path.

        Args:
            bfile (bytes): File content.
            user_id (int): ID of the user owning the file.
            extension (str): File extension (e.g., '.png').

        Returns:
            str: Full path to the saved file.
        """
        file_name = f'{user_id}_{time()}{extension}'
        file_path = join(self.base_path, file_name)

        async with aioopen(file_path, 'wb') as file:
            await file.write(bfile)

        return file_path

    async def delete(self, path: str) -> None:
        """
        Delete a file if it exists.

        Args:
            path (str): Path to the file to remove.
        """
        Path(path).unlink(missing_ok=True)
