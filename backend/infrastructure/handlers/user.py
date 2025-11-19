from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, File, UploadFile

from infrastructure.database.repositories.user import UserRepository
from infrastructure.database.uows.database_uow import DatabaseUnitOfWork
from infrastructure.dependencies import get_access_token, get_request_user
from infrastructure.dependency_injection_containers.database import DatabaseContainer
from infrastructure.http.update_chat_related_user import UpdateChatRelatedUser
from infrastructure.incoming_dtos import IncomingCreateUserDTO, IncomingUpdateUserDTO, UserIdsDTO
from infrastructure.file_storage import FileStorage
from infrastructure.security.default_hasher import DefaultHasher
from interface_adapters.controllers import (
    CreateUserController,
    GetUsersInfoController,
    SearchUsersController,
    UpdateAvatarController,
    UpdateUserController
)
from interface_adapters.outgoing_dtos import OutgoingUserDTO


user_router = APIRouter(prefix='/users')

@user_router.post('/')
@inject
async def create_user(
    user: IncomingCreateUserDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> OutgoingUserDTO:
    """
    Create a user.
    """
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
    user: dict = Depends(get_request_user),
) -> OutgoingUserDTO:
    """
    Get a requesting user.
    """
    return OutgoingUserDTO.from_dict(user)

@user_router.patch('/update')
@inject
async def update_user(
    user_data: IncomingUpdateUserDTO,
    user: dict = Depends(get_request_user),
    access_token: str = Depends(get_access_token),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> OutgoingUserDTO:
    """
    Update the user data.
    """
    async with database_uow:
        controller = UpdateUserController(
            user_id=user.get('id'),
            user_data=user_data.model_dump(),
            access_token=access_token,
            database_repo=UserRepository(session=database_uow.session),
            database_uow=database_uow,
            http_service=UpdateChatRelatedUser(),
        )

        return await controller.update_user()

@user_router.patch('/avatar')
@inject
async def update_avatar(
    avatar: UploadFile = File(...),
    user: dict = Depends(get_request_user),
    access_token: str = Depends(get_access_token),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
) -> dict:
    """
    Update the user avatar.
    """
    async with database_uow:
        controller = UpdateAvatarController(
            file=await avatar.read(),
            file_name=avatar.filename,
            user_id=user.get('id'),
            access_token=access_token,
            file_storage=FileStorage(),
            database_repo=UserRepository(session=database_uow.session),
            database_uow=database_uow,
            http_service=UpdateChatRelatedUser(),
        )

        return await controller.update_avatar()
    
@user_router.get('/search')
@inject
async def search(
    username: str,
    user: dict = Depends(get_request_user),
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
):
    """
    Search the users.
    """
    async with database_uow:
        controller = SearchUsersController(
            username=username,
            user=user,
            database_repo=UserRepository(session=database_uow.session)
        )

        return await controller.search_users()
    
@user_router.post('/get-users-info')
@inject
async def get_users_info(
    user_ids: UserIdsDTO,
    database_uow: DatabaseUnitOfWork = Depends(Provide[DatabaseContainer.unit_of_work]),
):
    """
    Technical endpoint that is used to get rich information 
    about users upon the creation of a chat.
    """
    async with database_uow:
        controller = GetUsersInfoController(
            user_ids=user_ids.model_dump(),
            database_repo=UserRepository(session=database_uow.session),
        )

        return await controller.get_users_info()
