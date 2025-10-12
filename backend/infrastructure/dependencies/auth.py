from dataclasses import asdict
from http import HTTPStatus

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.exceptions import UserNotFoundException
from application.use_cases import GetUserUseCase
from infrastructure.database.repositories import UserRepository
from infrastructure.database.uows import DatabaseUnitOfWork
from infrastructure.dependency_injection_containers import DatabaseContainer
from infrastructure.security import JWTTokenProvider
from interfaces.dto import UserOut


@inject
async def get_request_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> UserOut | None:
    async with database_uow:
        use_case = GetUserUseCase(
            access_token=credentials.credentials,
            database_repo=UserRepository(session=database_uow.session),
            jwt_provider=JWTTokenProvider(),
        )

        try:
            user = await use_case.execute()
        except UserNotFoundException as error:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(error))
        else:
            return UserOut.from_dict(asdict(user))
