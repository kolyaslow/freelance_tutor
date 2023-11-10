from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .user import User
    from .subject import Subject


class BaseMixin:
    _back_populates: str | None = None
    field_fk: str | None = 'id'
    _table_name: str

    @declared_attr
    def _create_fk(cls)-> Mapped[int]:
        return mapped_column(ForeignKey(f'{cls._table_name}.{cls.field_fk}'))

    @declared_attr
    def _create_relationship(cls):
        return relationship(
            f"{cls.__name__}",
            back_populates=cls._back_populates,
        )


class UserRelationMixin(BaseMixin):
    _table_name = 'user'
    @declared_attr
    def user_id(cls) -> Mapped[int]:

        return cls._create_fk

    @declared_attr
    def user(cls) -> Mapped['User']:

        return cls._create_relationship


class SubjectRelationMixin(BaseMixin):
    _table_name = 'subject'

    @declared_attr
    def subject_name(cls) -> Mapped[int]:
        return cls._create_fk

    @declared_attr
    def subject(cls) -> Mapped["Subject"]:
        return cls._create_relationship



class SubjectUserAssociation(
    SubjectRelationMixin,
    UserRelationMixin,

):
    pass

s = SubjectUserAssociation()
print()