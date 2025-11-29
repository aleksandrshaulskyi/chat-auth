from zoneinfo import ZoneInfo

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #BASE
    current_domain: str = 'http://localhost'
    min_username_length: int = 4
    min_password_length: int = 8
    messaging_backend_url: str = 'http://messaging_backend:8002'
    #SECURITY
    key: str = Field(validation_alias='KEY')
    algorithm: str = Field(validation_alias='ALGORITHM')
    #DB
    database_url: str = Field(validation_alias='DATABASE_URL')
    echo: bool = True
    #REDIS
    redis_url: str = Field(validation_alias='REDIS_URL')
    #TZ
    default_tz: ZoneInfo = ZoneInfo('Europe/Belgrade')
    #CORS
    cors_origins: list = ['http://localhost:3000']
    #MEDIA
    media_root: str = f'{current_domain}/media'
    display_media_root: str = 'media'
    allowed_extensions: set = {'.jpg', '.jpeg', '.png'}
    max_size: int = 2097152
    #METRICS
    opentelemetry_collector_url: str = Field(validation_alias='OPENTELEMETRY_COLLECTOR_URL')
    #LOGGING
    sessions_logger_name: str = 'application.sessions'
    users_logger_name: str = 'application.users'

    model_config = {
        'env_file': '.env',
        'extra': 'allow',
    }

settings = Settings()
