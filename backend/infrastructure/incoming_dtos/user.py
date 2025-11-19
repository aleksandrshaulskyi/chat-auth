from pydantic import BaseModel, ConfigDict, Field

from settings import settings


class IncomingCreateUserDTO(BaseModel):
    """
    This dataclass is used for the instance of a user that is retrieved from JWT.
    """
    username: str = Field(..., min_length=settings.min_username_length)
    password: str = Field(..., min_length=settings.min_password_length)
    email: str

    model_config = ConfigDict(from_attributes=True)


class IncomingUpdateUserDTO(BaseModel):
    username: str = Field(..., min_length=settings.min_username_length)
    email: str


class UserIdsDTO(BaseModel):
    user_ids: list
