from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import settings


def setup_middleware(application: FastAPI) -> None:
    """
    Adds middleware to application.
    """
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    