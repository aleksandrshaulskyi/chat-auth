from sqlalchemy import exists, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.user import UserRepositoryPort
from infrastructure.database.models import UserModel
from infrastructure.internal_dtos import InternalUserDTO


class UserRepository(UserRepositoryPort):
    """
    The repository that is responsible for all the database actions
    related to users.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository.

        Args:
            session (AsyncSession): An instance of AsyncSession.
        """
        self.session: AsyncSession = session

    async def create(self, user_data: dict) -> dict:
        """
        Create a user and return its DTO.

        Args:
            user_data (dict): Fields for the new user.

        Returns:
            dict: Serialized user DTO.
        """
        user_model = UserModel(**user_data)

        self.session.add(user_model)

        await self.session.flush()
        await self.session.refresh(user_model)

        return InternalUserDTO.model_validate(user_model).model_dump()
    
    async def check_if_exists(self, properties: dict) -> bool:
        """
        Check whether a user exists matching given properties.

        Args:
            properties (dict): Fields to filter by.

        Returns:
            bool: True if a matching user exists.
        """
        conditions = []
        supported_properties = {
            'id': UserModel.id,
            'email': UserModel.email,
            'username': UserModel.username,
        }

        for property, value in properties.items():
            column = supported_properties.get(property)

            if column is None:
                raise ValueError
            conditions.append(column == value)

        query = select(exists().where(*conditions))
        result = (await self.session.execute(query)).scalar()
        return result

    async def get_by_properties(self, properties: dict) -> dict | None:
        """
        Return a user matching given properties.

        Args:
            properties (dict): Fields to filter by.

        Returns:
            dict | None: User DTO or None if not found.
        """
        conditions = []
        supported_properties = {
            'id': UserModel.id,
            'email': UserModel.email,
            'username': UserModel.username,
        }

        for property, value in properties.items():
            column = supported_properties.get(property)

            if column is None:
                raise ValueError
            conditions.append(column == value)

        query = select(UserModel).where(*conditions)
        result = await self.session.execute(query)

        if (user_model := result.scalar_one_or_none()) is not None:
            return InternalUserDTO.model_validate(user_model).model_dump()
        return None
    
    async def get_by_ids(self, ids: list) -> list:
        """
        Return users by a list of IDs.

        Args:
            ids (list): List of user IDs.

        Returns:
            list: List of user DTOs.
        """
        query = select(UserModel).where(UserModel.id.in_(ids))
        result = await self.session.execute(query)

        if (user_models := result.scalars().all()):
            return [InternalUserDTO.model_validate(user_model).model_dump() for user_model in user_models]
        return []

    async def update_user(self, user_id: int, user_data: dict) -> dict | None:
        """
        Update a user and return its DTO.

        Args:
            user_id (int): User ID.
            user_data (dict): Fields to update.

        Returns:
            dict | None: Updated user DTO or None if not found.
        """
        if (user_model := await self.session.get(UserModel, user_id)) is not None:
            properties = {prop.key for prop in inspect(UserModel).mapper.column_attrs}

            for key, value in user_data.items():
                if key in properties:
                    setattr(user_model, key, value)

            await self.session.flush()
            await self.session.refresh(user_model)

            return InternalUserDTO.model_validate(user_model).model_dump()
        return None

    async def update_avatar(self, user_id: int, avatar_url: str) -> dict | None:
        """
        Update user's avatar URL.

        Args:
            user_id (int): User ID.
            avatar_url (str): New avatar URL.

        Returns:
            dict | None: Updated user DTO or None if not found.
        """
        user_model = await self.session.get(UserModel, user_id)

        if user_model is not None:
            user_model.avatar_url = avatar_url

            await self.session.flush()
            await self.session.refresh(user_model)

            return InternalUserDTO.model_validate(user_model).model_dump()
        return None

    async def search_users_by_username(self, username: str, user_username: str) -> list:
        """
        Search users by partial username match.

        Args:
            username (str): Username fragment to search for.
            user_username (str): Username to exclude.

        Returns:
            list: List of user DTOs.
        """
        query = select(UserModel).where(
            UserModel.username.contains(username) &
            ~(UserModel.username == user_username)
        )
        result = await self.session.execute(query)

        if (user_models := result.scalars().all()):
            return [InternalUserDTO.model_validate(user_model).model_dump() for user_model in user_models]
        return []
