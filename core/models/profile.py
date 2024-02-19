from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _id_unique = True  # установка уникальности первичного ключа
    _back_populates = "profile"

    fullname: Mapped[str | None]
    description: Mapped[str | None]

    balance: Mapped[float] = mapped_column(default=0)
