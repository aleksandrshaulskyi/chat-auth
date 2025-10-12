from sqlalchemy import inspect, select
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.ports import SessionRepositoryPort
from infrastructure.database.models import SessionModel
from infrastructure.dto import SessionDTO


class SessionRepository(SessionRepositoryPort):

    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self.session = session

    async def create_session(self, data: dict) -> dict:
        session_model = SessionModel(**data)

        self.session.add(session_model)

        await self.session.flush()
        await self.session.refresh(session_model)

        return SessionDTO.model_validate(session_model).model_dump()
    
    async def get_session(self, filters: dict) -> dict | None:
        query = select(SessionModel).filter_by(**filters)
        result = await self.session.execute(query)

        if (session_model := result.scalar_one_or_none()) is not None:
            return SessionDTO.model_validate(session_model).model_dump()
        
        return None
    
    async def get_sessions(self, filters: dict) -> dict | None:
        query = select(SessionModel).filter_by(**filters)
        result = await self.session.execute(query)

        if (session_models := result.unique().scalars().all()):
            return [SessionDTO.model_validate(session_model).model_dump() for session_model in session_models]

    async def update_session(self, session_id: int, data: dict) -> dict | None:
        if (session_model := await self.session.get(SessionModel, session_id)) is not None:
            properties = {prop.key for prop in inspect(SessionModel).mapper.column_attrs}

            for key, value in data.items():
                if key in properties:
                    setattr(session_model, key, value)

            await self.session.flush()
            await self.session.refresh(session_model)

            return SessionDTO.model_validate(session_model).model_dump()
        
        return None
