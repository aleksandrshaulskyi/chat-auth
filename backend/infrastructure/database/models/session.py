from datetime import datetime, timedelta

from sqlalchemy import Boolean, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from settings import settings

from infrastructure.database.models import BaseModel


class SessionModel(BaseModel):
    __tablename__ = 'sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(settings.default_tz), nullable=False)
    valid_through: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(settings.default_tz) + timedelta(hours=24))
    user_agent: Mapped[str] = mapped_column(String)
    access_token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    terminated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
