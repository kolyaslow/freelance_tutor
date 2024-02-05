from typing import Annotated

from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Subject
from core.db_helper import db_helper
from .schemas import AllowedValuesByName
from ..common.dependencies import get_item_db_by_id

async def get_subject(
    subject_name: Annotated[AllowedValuesByName, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Subject:
    subject = await get_item_db_by_id(
        session=session,
        item_id=subject_name,
        model_db=Subject
    )
    return subject