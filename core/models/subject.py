from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .subject_user_association import SubjectUserAssociation

class Subject(Base):
    primary_key_id = False
    name: Mapped[str] = mapped_column(primary_key=True)

    user_details: Mapped[list['SubjectUserAssociation']] = relationship(back_populates='subject')
