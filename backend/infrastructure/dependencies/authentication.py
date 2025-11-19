from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.use_cases import GetUserUseCase
from infrastructure.database.repositories import UserRepository
from infrastructure.database.uows import DatabaseUnitOfWork
from infrastructure.dependency_injection_containers import DatabaseContainer
from infrastructure.internal_dtos import InternalUserDTO
from infrastructure.security import JWTManager


@inject
async def get_request_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> InternalUserDTO:
    """
    The authentication dependency that extracts the user id from the provided credentials
    and attempts to retrieve a User based on them.
    """
    user_id = await JWTManager().get_user_id(token=credentials.credentials)

    async with database_uow:
        use_case = GetUserUseCase(
            user_id=user_id,
            database_repo=UserRepository(session=database_uow.session),
            jwt_manager=JWTManager(),
        )

        return InternalUserDTO(**await use_case.execute()).model_dump()

async def get_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str:
    """
    Return the access token from the provided credentials.
    """
    return credentials.credentials
