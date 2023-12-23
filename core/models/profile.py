from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Profile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    fullname: Mapped[str]
    description: Mapped[str]


