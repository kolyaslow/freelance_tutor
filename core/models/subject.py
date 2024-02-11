from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .order import Order


class Subject(Base):
    primary_key_id = False

    name: Mapped[str] = mapped_column(primary_key=True)

    __table_args__ = (
        CheckConstraint(
            name.in_(["mathematics", "informatics", "programming"]), name="name"
        ),
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="subjects",
        secondary="subject_user_association",
    )
    orders: Mapped["Order"] = relationship("Order")
