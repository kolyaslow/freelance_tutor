from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Order(Base):

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "subject_name",
            name="idx_unique_user_subject_order",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    subject_name: Mapped[int] = mapped_column(ForeignKey('subject.name'))
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped['User'] = relationship(back_populates='orders')
