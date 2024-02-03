from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from core.db_helper import db_helper
from core.models import Order
from ..common import crud as crud_common


async def get_order_by_id(
        order_id: int,
        session: AsyncSession = Depends(db_helper.session_dependency)
) -> Order:
    order = await crud_common.get_db_item_by_id(
        session=session,
        id_item=order_id,
        model_item=Order,
    )

    if order:
        return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND
    )

