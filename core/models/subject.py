from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Subject(Base):
    primary_key_id = False
    name: Mapped[str] = mapped_column(primary_key=True)
