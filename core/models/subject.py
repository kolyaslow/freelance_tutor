from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Subject(Base):
    name: Mapped[str] = mapped_column(primary_key=True)
