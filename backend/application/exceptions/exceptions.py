class AuthenticationException(Exception):
    'An exception that should be risen if something goes wrong while authentication process.'

    def __init__(self, details: dict | None = None) -> None:
        self.title = 'Authentication error'
        self.details = details


class DataIntegrityException(Exception):
    'An exception that should be risen if something goes wrong with data integrity.'

    def __init__(self, details: dict | None = None, constraint_name: str | None = None) -> None:
        self.title = 'Data integrity error'
        self.details = details
        self.constraint_name = constraint_name

    async def get_constraint_field_name(self) -> str:
        if self.constraint_name is None:
            return ''
        try:
            return self.constraint_name.split('_')[1]
        except IndexError:
            return ''


class UserNotFoundException(DataIntegrityException):
    'An exception risen if a user was not found.'


class UserAlreadyExistsException(DataIntegrityException):
    'An exception risen if a user with provided credentials already exists.'


class InvalidPasswordException(AuthenticationException):
    'An exception risen if password is invalid.'


class InvalidJWTException(AuthenticationException):
    'An exception risen if token is invalid.'


class FileSizeException(DataIntegrityException):
    'An exception risen if a file size exceeds the allowed limit.'


class FileExtensionException(DataIntegrityException):
    'An exception risen if a file extension is not allowed.'
