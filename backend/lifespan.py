from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.dependency_injection_containers import DatabaseContainer


@asynccontextmanager
async def lifespan(application: FastAPI):
    database_container = DatabaseContainer()
    database_container.wire(
        modules=['infrastructure.handlers.user', 'infrastructure.handlers.session']
    )

    yield
