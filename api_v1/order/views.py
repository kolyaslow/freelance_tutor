from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, APIRouter, status, HTTPException

from core.db_helper import db_helper
from .schemas import CreateOrder, ShowOrder
from core.models import User, Order
from ..common.dependencies import user_rights
from ..common import crud as crud_common
from .dependencies import get_order_by_id

router = APIRouter()


@router.post(
        '/create_order',
        response_model=ShowOrder,
        status_code=status.HTTP_201_CREATED
)
async def create_order(
        order_in: CreateOrder,
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(user_rights.checking_customer),
) -> Order:
    order_in.user_id = user.id

    return await crud_common.create_db_item(
            session=session,
            model_db=Order,
            data=order_in,
    )


@router.delete(
        '/delete_order/{order_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(user_rights.checking_customer)]
)
async def delete_order(
        order: Order = Depends(get_order_by_id),
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    await crud_common.delete_db_item(
        session=session,
        delete_item=order,
    )