from fastapi import FastAPI

from infrastructure.handlers import session_router, user_router


def setup_handlers(application: FastAPI) -> None:
    """
    Include routers to application.
    """
    application.include_router(session_router)
    application.include_router(user_router)
