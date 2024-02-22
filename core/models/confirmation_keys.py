from sqlalchemy.orm import Mapped

from core.models import Base
from core.models.mixins import UserRelationMixin


class ConfirmationKeys(Base, UserRelationMixin):
    _back_populates = "confirmation_keys"
    email_confirmation_code: Mapped[str]
