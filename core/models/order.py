from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Order(Base, UserRelationMixin):

    _back_populates = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[int] = mapped_column(ForeignKey("subject.name"))
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
