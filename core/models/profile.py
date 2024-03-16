from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _id_unique = True  # установка уникальности первичного ключа
    _back_populates = "profile"

    fullname: Mapped[str | None]
    description: Mapped[str | None]
    rating: Mapped[float] = mapped_column(
        Float,
        default=5,
        server_default="5",
    )

    balance: Mapped[float] = mapped_column(default=0)
