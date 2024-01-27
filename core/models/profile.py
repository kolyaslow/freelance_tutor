from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)

    fullname: Mapped[str | None]
    description: Mapped[str | None]

    user: Mapped['User'] = relationship(back_populates='profile')
