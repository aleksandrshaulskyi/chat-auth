from dataclasses import asdict
from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, Response

from infrastructure.database.repositories import SessionRepository, UserRepository
from infrastructure.database.uows import DatabaseUnitOfWork
from infrastructure.dependencies import get_request_user
from infrastructure.dependency_injection_containers.database import DatabaseContainer
from infrastructure.dto import CreateSessionDTO, RefreshDataDTO
from infrastructure.security import DefaultHasher, JWTTokenProvider
from interfaces.controllers import CreateSessionController, RefreshSessionController, TerminateAllSessionsController, TerminateSessionController
from interfaces.dto import UserOut


session_router = APIRouter(prefix='/sessions')

@session_router.post('/')
@inject
async def create_session(
    request: Request,
    session_data: CreateSessionDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> JSONResponse:
    async with database_uow:
        user_agent = request.headers.get('user-agent')

        session_data = session_data.model_dump()
        session_data.update({'user_agent': user_agent})

        controller = CreateSessionController(
            session_data=session_data,
            session_database_repo=SessionRepository(session=database_uow.session),
            user_database_repo=UserRepository(session=database_uow.session),
            default_hasher=DefaultHasher(),
            jwt_provider=JWTTokenProvider(),
            database_uow=database_uow,
        )

        session_out = asdict(await controller.create_session())

        return JSONResponse(content=session_out)

@session_router.post('/refresh')
@inject
async def refresh_session(
    request: Request,
    refresh_data: RefreshDataDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> JSONResponse:
    async with database_uow:
        user_agent = request.headers.get('user-agent')

        session_data = refresh_data.model_dump()
        session_data.update({'user_agent': user_agent})

        controller = RefreshSessionController(
            session_data=session_data,
            session_database_repo=SessionRepository(session=database_uow.session),
            jwt_provider=JWTTokenProvider(),
            database_uow=database_uow,
        )

        if (session := await controller.refresh_session()) is not None:
            session_out = asdict(session)
        else:
            session_out = None

        return JSONResponse(content=session_out)
    
@session_router.post('/terminate')
@inject
async def terminate_session(
    request: Request,
    user: UserOut = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> JSONResponse:
    async with database_uow:
        user_agent = request.headers.get('user-agent')

        session_data = {'user_id': user.id, 'user_agent': user_agent}

        controller = TerminateSessionController(
            session_data=session_data,
            database_repo=SessionRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        await controller.terminate_session()

        return Response(status_code=HTTPStatus.NO_CONTENT)

@session_router.post('/terminate-all')
@inject
async def terminate_all_sessions(
    user: UserOut = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work])
) -> None:
    async with database_uow:
        controller = TerminateAllSessionsController(
            user_id=user.id,
            database_repo=SessionRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        await controller.terminate_all_sessions()

        return Response(status_code=HTTPStatus.NO_CONTENT)
