from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Session:
    id: int | None
    user_id: int
    created_at: datetime
    valid_through: datetime
    user_agent: str | None
    access_token: str
    refresh_token: str
    terminated: bool

    @property
    def is_ongoing(self) -> bool:
        return datetime.now() < self.valid_through
    
    def prolong(self, access_token: str, refresh_token: str) -> None:
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.valid_through = datetime.now() + timedelta(hours=24)

    def terminate(self) -> None:
        self.valid_through = datetime.now()
        self.terminated = True
