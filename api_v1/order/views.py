from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common.dependencies import user_rights
from core.db_helper import db_helper
from core.models import Order, User

from ..common import crud as crud_common
from . import crud as crud_order
from .dependencies import get_order_by_id
from .schemas import CreateOrder, OrderingWithCustomer, ShowOrder

router = APIRouter()


@router.post(
    "/create_order", response_model=ShowOrder, status_code=status.HTTP_201_CREATED
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


@router.get("/get_all_orders", response_model=list[ShowOrder])
async def get_all_orders(
    user: User = Depends(user_rights.checking_customer),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[Order]:
    """Получение заказчиком всех своих заказов"""
    orders = await crud_order.get_all_orders(
        session=session,
        user=user,
    )
    return orders


@router.get("/getting_orders_for_tutor", response_model=list[OrderingWithCustomer])
async def getting_orders_for_tutor(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(user_rights.checking_tutor),
) -> list[OrderingWithCustomer]:
    orders = await crud_order.getting_orders_for_tutor(
        session=session,
        user_id=user.id,
    )
    return orders


@router.delete(
    "/delete_order/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rights.checking_customer)],
)
async def delete_order(
    order: Order = Depends(get_order_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud_common.delete_db_item(
        session=session,
        delete_item=order,
    )
