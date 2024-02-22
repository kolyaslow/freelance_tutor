from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Subject

from ..common import dependencies
from .schemas import AllowedValuesByName


async def get_subject(
    subject_name: Annotated[AllowedValuesByName, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Subject:
    subject = await dependencies.get_item_db_by_id(
        session=session, item_id=subject_name, model_db=Subject
    )
    return subject
