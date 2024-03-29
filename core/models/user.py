from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import db_helper
from core.models.base import Base

if TYPE_CHECKING:
    from .confirmation_keys import ConfirmationKeys
    from .order import Order
    from .profile import Profile
    from .subject import Subject


class User(SQLAlchemyBaseUserTable[int], Base):
    role: Mapped[str] = mapped_column(
        String(length=9),
        nullable=False,
    )
    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="users",
        secondary="subject_user_association",
    )

    profile: Mapped["Profile"] = relationship(back_populates="user")
    orders: Mapped["Order"] = relationship(back_populates="user")
    confirmation_keys: Mapped["ConfirmationKeys"] = relationship(back_populates="user")


async def get_user_db(session: AsyncSession = Depends(db_helper.session_dependency)):
    yield SQLAlchemyUserDatabase(session, User)
