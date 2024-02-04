from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from core.db_helper import db_helper
from core.models import Order
from ..common import crud as crud_common
from ..common.dependencies import get_item_db_by_id


async def get_order_by_id(
        order_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> Order:
    return await get_item_db_by_id(
        session=session,
        item_id=order_id,
        model_db=Order,
    )

