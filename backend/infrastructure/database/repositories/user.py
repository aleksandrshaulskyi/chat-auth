from sqlalchemy import inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from application.exceptions import UserAlreadyExistsException, UserNotFoundException
from application.ports.user import UserRepositoryPort
from infrastructure.database.models.user import UserModel
from infrastructure.dto.user import UserDTO


class UserRepository(UserRepositoryPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def create(self, user_data: dict) -> dict:
        user_model = UserModel(**user_data)

        self.session.add(user_model)

        try:
            await self.session.flush()
        except IntegrityError as exception:
            raise UserAlreadyExistsException(constraint_name=exception.orig.diag.constraint_name)

        await self.session.refresh(user_model)

        return UserDTO.model_validate(user_model).model_dump()
    
    async def get_by_username(self, username: str) -> dict | None:
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)
        if (user_model := result.scalar_one_or_none()) is not None:

            return UserDTO.model_validate(user_model).model_dump()
        return None
    
    async def get_by_id(self, id: int) -> dict | None:
        if (user_model := await self.session.get(UserModel, id)) is not None:
            return UserDTO.model_validate(user_model).model_dump()
        
        return None
    
    async def update_user(self, user_id: int, user_data: dict) -> dict | None:
        if (user_model := await self.session.get(UserModel, user_id)) is not None:
            properties = {prop.key for prop in inspect(UserModel).mapper.column_attrs}

            for key, value in user_data.items():
                if key in properties:
                    setattr(user_model, key, value)

            try:
                await self.session.flush()
            except IntegrityError as exception:
                raise UserNotFoundException(constraint_name=exception.orig.diag.constraint_name)
            await self.session.refresh(user_model)

            return UserDTO.model_validate(user_model).model_dump()
        return None

    async def update_avatar(self, user_id: int, avatar_url: str) -> None:
        query = update(UserModel).where(UserModel.id==user_id).values(avatar_url=avatar_url)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise UserNotFoundException('A user with provided id was not found.')
