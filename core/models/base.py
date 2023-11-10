import re

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
        words_in_name = re.findall('[A-Z][a-z]*', cls.__name__)
        snake_case_name = '_'.join(word.lower() for word in words_in_name)
        return snake_case_name
