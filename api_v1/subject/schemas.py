from enum import Enum
from pydantic import BaseModel


class AllowedValuesByName(str, Enum):
    mathematics = "mathematics"
    informatics = "informatics"
    programming = "programming"


class Base(BaseModel):
    name: AllowedValuesByName


class CreateSubject(Base):
    pass

class SubjectRead(Base):
    pass