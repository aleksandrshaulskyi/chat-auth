from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from settings import settings

from infrastructure.database.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    avatar_url: Mapped[str] = mapped_column(String, default=f'{settings.media_root}/default.jpg')
