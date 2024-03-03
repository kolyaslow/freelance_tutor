from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class BaseMixin:
    _back_populates: str | None = None
    _field_fk: str = "id"
    _table_name: str
    _id_unique: bool = False

    @classmethod
    def _create_fk(cls) -> Mapped[int | str]:
        return mapped_column(
            ForeignKey(f"{cls._table_name}.{cls._field_fk}"),
            unique=cls._id_unique,
        )

    @classmethod
    def _create_relationship(cls):
        return relationship(
            cls._table_name.title(),
            back_populates=cls._back_populates,
        )


class UserRelationMixin(BaseMixin):
    """
    Создание FK с название user_id и relationship с нзванием user.
    """

    _table_name = "user"

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return cls._create_fk()

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return cls._create_relationship()
