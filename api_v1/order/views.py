from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status

from core.db_helper import db_helper
from .schemas import CreateOrder
from core.models import User, Order
from ..common.dependencies import user_rights
from ..common import crud as crud_common

router = APIRouter()


@router.post(
        '/create_order',
        response_model=CreateOrder,
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


@router.post(
        '/create_order',
        status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order():
        pass