from sqlalchemy import exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.user import UserRepositoryPort
from infrastructure.database.models import UserModel
from infrastructure.exceptions import InvalidDatabaseFilters
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
        statement = insert(UserModel).values(**user_data).returning(*UserModel.__table__.columns)

        result = await self.session.execute(statement=statement)
        row = result.mappings().one()

        return InternalUserDTO.model_validate(row).model_dump()

    async def check_if_exists(self, properties: dict) -> bool:
        """
        Check whether a user exists matching given properties.

        Args:
            properties (dict): Fields to filter by.

        Returns:
            bool: True if a matching user exists.
        """
        supported_properties = {
            'id': UserModel.__table__.columns.id,
            'email': UserModel.__table__.columns.email,
            'username': UserModel.__table__.columns.username,
        }

        try:
            conditions = {supported_properties[property] == value for property, value in properties.items()}
        except KeyError:
            raise InvalidDatabaseFilters(
                title='Invalid filters provided.',
                details={
                    'Invalid filters provided.': 'The invalid filters were provided to the database repository.',
                },
            )

        statement = select(exists().where(*conditions))
        result = (await self.session.execute(statement=statement)).scalar_one()
        return result

    async def get_by_properties(self, properties: dict) -> dict | None:
        """
        Return a user matching given properties.

        Args:
            properties (dict): Fields to filter by.

        Returns:
            dict | None: User DTO or None if not found.
        """
        supported_properties = {
            'id': UserModel.__table__.columns.id,
            'email': UserModel.__table__.columns.email,
            'username': UserModel.__table__.columns.username,
        }

        try:
            conditions = {supported_properties[property] == value for property, value in properties.items()}
        except KeyError:
            raise InvalidDatabaseFilters(
                title='Invalid filters provided.',
                details={
                    'Invalid filters provided.': 'The invalid filters were provided to the database repository.',
                },
            )

        statement = select(UserModel.__table__).where(*conditions)
        result = await self.session.execute(statement=statement)

        if (row := result.mappings().one_or_none()) is not None:
            return InternalUserDTO.model_validate(row).model_dump()
        return None
    
    async def get_by_ids(self, ids: list) -> list:
        """
        Return users by a list of IDs.

        Args:
            ids (list): List of user IDs.

        Returns:
            list: List of user DTOs.
        """
        statement = select(UserModel.__table__).where(UserModel.__table__.columns.id.in_(ids))
        result = await self.session.execute(statement=statement)

        if (rows := result.mappings().all()):
            return [InternalUserDTO.model_validate(row).model_dump() for row in rows]
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
        statement = update(
            UserModel.__table__,
        ).where(
            UserModel.__table__.columns.id == user_id,
        ).values(
            **user_data,
        ).returning(
            *UserModel.__table__.columns,
        )

        result = await self.session.execute(statement=statement)

        if (row := result.mappings().one_or_none()) is not None:
            return InternalUserDTO.model_validate(row).model_dump()
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
        statement = update(
            UserModel.__table__,
        ).where(
            UserModel.__table__.columns.id == user_id,
        ).values(
            {'avatar_url': avatar_url},
        ).returning(
            *UserModel.__table__.columns,
        )

        result = await self.session.execute(statement=statement)
        if (row := result.mappings().one_or_none()) is not None:
            return InternalUserDTO.model_validate(row).model_dump()
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
        statement = select(
            UserModel.__table__,
        ).where(
            UserModel.__table__.columns.username.contains(username) & 
            ~(UserModel.__table__.columns.username == user_username),
        )

        result = await self.session.execute(statement=statement)

        if (rows := result.mappings().all()):
            return [InternalUserDTO.model_validate(row).model_dump() for row in rows]
        return []
