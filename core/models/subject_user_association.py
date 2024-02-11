from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, UniqueConstraint

from .base import Base


class SubjectUserAssociation(Base):

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "subject_name",
            name="idx_unique_user_subject",
        ),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    subject_name: Mapped[str] = mapped_column(ForeignKey("subject.name"))
