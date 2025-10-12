from pydantic import BaseModel, ConfigDict, Field

from settings import settings


class UserDTO(BaseModel):
    id: int | None = None
    username: str = Field(..., min_length=settings.min_username_length)
    password: str = Field(..., min_length=settings.min_password_length)
    email: str
    avatar_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserDTO(BaseModel):
    username: str = Field(..., min_length=settings.min_username_length)
    email: str
