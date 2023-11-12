from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .subject import Subject



class SubjectUserAssociation(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    subject_name: Mapped[str] = mapped_column(ForeignKey('subject.name'))

    user: Mapped['User'] = relationship(back_populates='subject_details')
    subject: Mapped['Subject'] = relationship(back_populates='user_details')


