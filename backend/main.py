from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from settings import settings

from application.exceptions import AuthenticationException, DataIntegrityException
from infrastructure.dependency_injection_containers.database import DatabaseContainer
from infrastructure.exception_handlers import (
    authentication_exception_handler,
    data_integrity_exception_handler,
    pydantic_validation_exception_handler,
)
from infrastructure.handlers import session_router, user_router


application = FastAPI()

database_container = DatabaseContainer()
database_container.wire(modules=['infrastructure.handlers.user', 'infrastructure.handlers.session'])

application.database_container = database_container

application.include_router(user_router)
application.include_router(session_router)

application.add_exception_handler(AuthenticationException, authentication_exception_handler)
application.add_exception_handler(DataIntegrityException, data_integrity_exception_handler)
application.add_exception_handler(RequestValidationError, pydantic_validation_exception_handler)

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
