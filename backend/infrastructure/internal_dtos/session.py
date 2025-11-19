from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InternalSessionDTO(BaseModel):
    """
    The dataclass that is responsible for transmitting session data internally.
    """
    id: int | None
    user_id: int
    created_at: datetime
    valid_through: datetime
    user_agent: str | None
    access_token: str
    refresh_token: str
    terminated: bool | None

    model_config = ConfigDict(from_attributes=True)
