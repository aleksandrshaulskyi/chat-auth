from domain.exceptions import BaseException


class ApplicationException(BaseException):
    """
    This is the base exception for all of the exceptions that can be raisen
    on the application layer.
    """


class AuthenticationException(ApplicationException):
    """
    Should be raisen if an error occurs while authenticating a user.
    """


class SessionDoesNotExistException(ApplicationException):
    """
    Should be raisen if there is no ongoing session exists for the requesting user.
    """


class UserAlreadyExistsException(ApplicationException):
    """
    Should be raisen if a user with such data (username and email) already exists.
    """


class UserNotFoundException(ApplicationException):
    """
    Should be raisen if a user with the provided filters was not found.
    """


class ChatsServerUnavailable(ApplicationException):
    """
    Should be raisen if there was no response from the server that
    is responsible for updating chats.
    """


class FileSizeException(ApplicationException):
    """
    Should be raisen if the file size exceeds the limit.
    """


class FileExtensionException(ApplicationException):
    """
    Should be raisen if provided file extension is not supported.
    """
