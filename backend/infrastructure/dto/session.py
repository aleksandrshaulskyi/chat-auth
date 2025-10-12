from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from settings import settings


class SessionDTO(BaseModel):
    id: int | None
    user_id: int
    created_at: datetime
    valid_through: datetime
    user_agent: str | None
    access_token: str
    refresh_token: str
    terminated: bool | None

    model_config = ConfigDict(from_attributes=True)


class CreateSessionDTO(BaseModel):
    username: str = Field(..., min_length=settings.min_username_length)
    password: str = Field(..., min_length=settings.min_password_length)
