from pydantic import BaseModel, Field

from settings import settings


class IncomingCreateSessionDTO(BaseModel):
    username: str = Field(..., min_length=settings.min_username_length)
    password: str = Field(..., min_length=settings.min_password_length)


class IncomingRefreshSessionDataDTO(BaseModel):
    refresh_token: str
