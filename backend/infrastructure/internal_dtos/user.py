from pydantic import BaseModel, ConfigDict, Field

from settings import settings


class InternalUserDTO(BaseModel):
    """
    This dataclass is intended for the internal transmission of data that belongs to
    the User entity.
    """
    id: int
    username: str = Field(..., min_length=settings.min_username_length)
    password: str = Field(..., min_length=settings.min_password_length)
    email: str
    avatar_url: str

    model_config = ConfigDict(from_attributes=True)
