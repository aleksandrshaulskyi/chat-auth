from fastapi import FastAPI

from infrastructure.exception_handlers import setup_exception_handlers
from infrastructure.handlers import setup_handlers
from infrastructure.middleware import setup_middleware
from lifespan import lifespan


def compose_application() -> FastAPI:
    """
    Compose the application.

    - Setup routers.
    - Setup exception handlers.
    - Setup middleware.

    Returns:
        application: An instance of FastAPI application.
    """
    application = FastAPI(lifespan=lifespan)

    setup_handlers(application=application)
    setup_exception_handlers(application=application)
    setup_middleware(application=application)

    return application
