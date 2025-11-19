from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from application.exceptions import ApplicationException
from infrastructure.exception_handlers import application_exception_handler, request_validation_exception_handler


def setup_exception_handlers(application: FastAPI) -> None:
    """
    Adds all the exception handlers.
    """
    application.add_exception_handler(ApplicationException, application_exception_handler)
    application.add_exception_handler(RequestValidationError, request_validation_exception_handler)
