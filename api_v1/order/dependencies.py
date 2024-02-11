from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Order

from ..common.dependencies import get_item_db_by_id


async def get_order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Order:
    return await get_item_db_by_id(
        session=session,
        item_id=order_id,
        model_db=Order,
    )
