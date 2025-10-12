from passlib.hash import pbkdf2_sha256

from application.exceptions import InvalidPasswordException
from application.ports import DefaultHasherPort


class DefaultHasher(DefaultHasherPort):

    async def hash(self, value: str | int) -> str:
        return pbkdf2_sha256.hash(value)

    async def verify(self, value: str | int, hash: str | int) -> bool:
        if not pbkdf2_sha256.verify(value, hash):
            raise InvalidPasswordException
