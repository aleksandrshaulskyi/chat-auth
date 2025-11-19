from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.ports import SessionRepositoryPort
from infrastructure.database.models import SessionModel
from infrastructure.internal_dtos import InternalSessionDTO


class SessionRepository(SessionRepositoryPort):
    """
    The repository that is responsible for all database actions
    related to sessions.
    """

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        """
        Initialize the repository.

        Args:
            session (async_sessionmaker[AsyncSession]): An instance of a session.
        """
        self.session = session

    async def create_session(self, data: dict) -> dict:
        """
        Create a session and return its DTO.

        Args:
            data (dict): Fields for the new session.

        Returns:
            dict: Serialized session DTO.
        """
        session_model = SessionModel(**data)

        self.session.add(session_model)

        await self.session.flush()
        await self.session.refresh(session_model)

        return InternalSessionDTO.model_validate(session_model).model_dump()
    
    async def get_session(self, filters: dict) -> dict | None:
        """
        Return a single session matching filters.

        Args:
            filters (dict): Query filters.

        Returns:
            dict | None: Session DTO or None if not found.
        """
        query = select(SessionModel).filter_by(**filters)
        result = await self.session.execute(query)

        if (session_model := result.scalar_one_or_none()) is not None:
            return InternalSessionDTO.model_validate(session_model).model_dump()
        
        return None
    
    async def get_sessions(self, filters: dict) -> dict | None:
        """
        Return all sessions matching filters.

        Args:
            filters (dict): Query filters.

        Returns:
            list[dict] | None: List of session DTOs or None if empty.
        """
        query = select(SessionModel).filter_by(**filters)
        result = await self.session.execute(query)

        if (session_models := result.unique().scalars().all()):
            return [InternalSessionDTO.model_validate(session_model).model_dump() for session_model in session_models]

    async def update_session(self, session_id: int, data: dict) -> dict | None:
        """
        Update a session and return its DTO.

        Args:
            session_id (int): Session identifier.
            data (dict): Fields to update.

        Returns:
            dict | None: Updated session DTO or None if not found.
        """
        if (session_model := await self.session.get(SessionModel, session_id)) is not None:
            properties = {prop.key for prop in inspect(SessionModel).mapper.column_attrs}

            for key, value in data.items():
                if key in properties:
                    setattr(session_model, key, value)

            await self.session.flush()
            await self.session.refresh(session_model)

            return InternalSessionDTO.model_validate(session_model).model_dump()
        
        return None
