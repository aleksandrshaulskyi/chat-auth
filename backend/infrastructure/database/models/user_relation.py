from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import BaseModel, UserModel


class UserRelationModel(BaseModel):
    __tablename__ = 'user_relations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_one_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_two_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_one: Mapped[UserModel] = relationship(UserModel, foreign_keys=[user_one_id])
    user_two: Mapped[UserModel] = relationship(UserModel, foreign_keys=[user_two_id])

    __table_args__ = (
        UniqueConstraint('user_one_id', 'user_two_id', name='unique_users_relation'),
    )
