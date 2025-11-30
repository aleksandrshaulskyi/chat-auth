from domain.exceptions import BaseException


class InfrastructureException(BaseException):
    """
    This is the base exception for all of the exceptions that can be raisen
    on the infrastructure layer.
    """


class InvalidDatabaseFilters(InfrastructureException):
    """
    Should be raisen if invalid set of filters were provided to the repository.
    """
