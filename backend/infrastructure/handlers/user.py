from asyncio import sleep
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, File, UploadFile

from infrastructure.database.repositories.user import UserRepository
from infrastructure.database.uows.database_uow import DatabaseUnitOfWork
from infrastructure.dependencies import get_request_user
from infrastructure.dependency_injection_containers.database import DatabaseContainer
from infrastructure.dto import UserDTO, UpdateUserDTO
from infrastructure.file_storage import FileStorage
from infrastructure.security.default_hasher import DefaultHasher
from interfaces.controllers import CreateUserController, UpdateAvatarController, UpdateUserController
from interfaces.dto import UserOut


user_router = APIRouter(prefix='/users')

@user_router.post('/')
@inject
async def create_user(
    user: UserDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> UserOut:
    await sleep(4)
    async with database_uow:
        controller = CreateUserController(
            user_data=user.model_dump(),
            default_hasher=DefaultHasher(),
            database_repo=UserRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        return await controller.create_user()

@user_router.get('/me')
async def get_user(
    user: UserOut = Depends(get_request_user),
) -> UserOut:
    return user

@user_router.patch('/update')
@inject
async def update_user(
    user_data: UpdateUserDTO,
    user: UserOut = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> UserOut:
    await sleep(4)
    async with database_uow:
        user_data = user_data.model_dump()
        controller = UpdateUserController(
            user=user,
            user_data=user_data,
            database_repo=UserRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        return await controller.update_user()

@user_router.patch('/avatar')
@inject
async def update_avatar(
    avatar: UploadFile = File(...),
    user: UserOut = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> dict:
    async with database_uow:
        controller = UpdateAvatarController(
            file=await avatar.read(),
            file_name=avatar.filename,
            user_id=user.id,
            file_storage=FileStorage(),
            database_repo=UserRepository(session=database_uow.session),
            database_uow=database_uow,
        )

        return await controller.update_avatar()
