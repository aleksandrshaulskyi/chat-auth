from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from infrastructure.database.main import create_engine, create_session_factory
from infrastructure.database.uows.database_uow import DatabaseUnitOfWork


class DatabaseContainer(DeclarativeContainer):
    engine = Singleton(create_engine)
    session_factory = Singleton(create_session_factory, engine=engine)

    unit_of_work = Factory(DatabaseUnitOfWork, session_factory)
