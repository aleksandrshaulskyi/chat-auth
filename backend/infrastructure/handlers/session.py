from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request
from fastapi.responses import Response

from infrastructure.database.repositories import SessionRepository, UserRepository
from infrastructure.database.uows import DatabaseUnitOfWork
from infrastructure.dependencies import get_request_user
from infrastructure.dependency_injection_containers.database import DatabaseContainer
from infrastructure.incoming_dtos import IncomingCreateSessionDTO, IncomingRefreshSessionDataDTO
from infrastructure.internal_dtos import InternalUserDTO
from infrastructure.security import DefaultHasher, JWTManager
from interface_adapters.controllers import (
    CreateSessionController,
    RefreshSessionController,
    TerminateAllSessionsController,
    TerminateSessionController,
)
from interface_adapters.outgoing_dtos import OutgoingSessionDTO


session_router = APIRouter(prefix='/sessions')

@session_router.post('/')
@inject
async def create_session(
    request: Request,
    session_data: IncomingCreateSessionDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> OutgoingSessionDTO:
    """
    Create a session for user.
    """
    async with database_uow:
        controller = CreateSessionController(
            session_data=session_data.model_dump(),
            user_agent=request.headers.get('user-agent'),
            session_database_repo=SessionRepository(session=database_uow.session),
            user_database_repo=UserRepository(session=database_uow.session),
            default_hasher=DefaultHasher(),
            jwt_manager=JWTManager(),
            database_uow=database_uow,
        )

        return await controller.create_session()

@session_router.post('/refresh')
@inject
async def refresh_session(
    request: Request,
    refresh_data: IncomingRefreshSessionDataDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> OutgoingSessionDTO:
    """
    Refresh an ongoing session.
    """
    async with database_uow:
        controller = RefreshSessionController(
            session_data=refresh_data.model_dump(),
            user_agent=request.headers.get('user-agent'),
            session_database_repo=SessionRepository(session=database_uow.session),
            jwt_manager=JWTManager(),
            database_uow=database_uow,
        )

        return await controller.refresh_session()

@session_router.post('/terminate')
@inject
async def terminate_session(
    request: Request,
    user: dict = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> Response:
    """
    Terminate a session for a provided user agent.
    """
    async with database_uow:
        controller = TerminateSessionController(
            user_id=user.get('id'),
            user_agent = request.headers.get('user-agent'),
            database_repo=SessionRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        await controller.terminate_session()

        return Response(status_code=HTTPStatus.NO_CONTENT)

@session_router.post('/terminate-all')
@inject
async def terminate_all_sessions(
    user: dict = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> None:
    """
    Terminate all sessions of a requesting user.
    """
    async with database_uow:
        controller = TerminateAllSessionsController(
            user_id=user.get('id'),
            database_repo=SessionRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        await controller.terminate_all_sessions()

        return Response(status_code=HTTPStatus.NO_CONTENT)
