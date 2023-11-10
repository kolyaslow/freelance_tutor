from sqlalchemy import Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True
    primary_key_id: bool = True

    @declared_attr
    def id(cls):
        if cls.primary_key_id:
            return mapped_column(Integer, primary_key=True)
        else:
            return None

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()