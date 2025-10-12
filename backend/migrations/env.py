from asyncio import run
from logging.config import fileConfig
from alembic import context
from settings import settings
from infrastructure.database.main import create_engine
from infrastructure.database.models.base import BaseModel

config = context.config
config.set_main_option('sqlalchemy.url', settings.database_url)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(sync_connection) -> None:
    context.configure(connection=sync_connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    engine = create_engine()
    async with engine.connect() as async_conn:
        await async_conn.run_sync(do_run_migrations)

def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run(run_migrations_online())

run_migrations()