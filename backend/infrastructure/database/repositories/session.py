from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports import SessionRepositoryPort
from infrastructure.database.models import SessionModel
from infrastructure.internal_dtos import InternalSessionDTO


class SessionRepository(SessionRepositoryPort):
    """
    The repository that is responsible for all database actions
    related to sessions.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository.

        Args:
            session (AsyncSession): An instance of a session.
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
        statement = insert(SessionModel).values(**data).returning(*SessionModel.__table__.columns)

        result = await self.session.execute(statement=statement)
        row = result.mappings().one()

        return InternalSessionDTO.model_validate(row).model_dump()
    
    async def get_session(self, filters: dict) -> dict | None:
        """
        Return a single session matching filters.

        Args:
            filters (dict): Query filters.

        Returns:
            dict | None: Session DTO or None if not found.
        """
        statement = select(SessionModel.__table__).filter_by(**filters)
        result = await self.session.execute(statement=statement)

        if (row := result.mappings().one_or_none()) is not None:
            return InternalSessionDTO.model_validate(row).model_dump()
        
        return None
    
    async def get_sessions(self, filters: dict) -> dict | None:
        """
        Return all sessions matching filters.

        Args:
            filters (dict): Query filters.

        Returns:
            list[dict] | None: List of session DTOs or None if empty.
        """
        statement = select(SessionModel.__table__).filter_by(**filters)
        result = await self.session.execute(statement=statement)

        if (rows := result.mappings().all()):
            return [InternalSessionDTO.model_validate(row).model_dump() for row in rows]
        return None

    async def update_session(self, session_id: int, data: dict) -> dict | None:
        """
        Update a session and return its DTO.

        Args:
            session_id (int): Session identifier.
            data (dict): Fields to update.

        Returns:
            dict | None: Updated session DTO or None if not found.
        """
        statement = update(
            SessionModel.__table__,
        ).where(
            SessionModel.__table__.columns.id == session_id,
        ).values(
            **data,
        ).returning(
            *SessionModel.__table__.columns,
        )

        result = await self.session.execute(statement=statement)

        if (row := result.mappings().one_or_none()) is not None:
            return InternalSessionDTO.model_validate(row).model_dump()
        return None
    
    async def terminate_sessions(self, ids: set) -> None:
        """
        Terminate sessions with provided ids.

        Args:
            ids (set): A set of ids of the sessions that need to be terminated.
        """
        statement = update(
            SessionModel.__table__,
        ).where(
            SessionModel.__table__.columns.id.in_(ids),
        ).values(
            {'terminated': True},
        )

        await self.session.execute(statement=statement)
