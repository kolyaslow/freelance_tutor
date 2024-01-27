from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Subject
from core.db_helper import db_helper
from . import crud


async def get_subject(
    # validate by AllowedValuesByName
    subject_name: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Subject:
    subject = await crud.get_subject(subject_name=subject_name, session=session)
    if subject:
        return subject
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {subject_name} not found!",
    )