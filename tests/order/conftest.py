import asyncio
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common import crud as crud_common
from api_v1.order.schemas import CreateOrder
from core.models import Order


@pytest.fixture
async def order(register_customer: dict):
    """Готовая модель заказа, для получения парамеров в тестах"""
    order = Order(
        id=1,
        user_id=register_customer["id"],
        subject_name="informatics",
        description="Первый заказ",
        is_active=True,
    )
    return order


@pytest.fixture
async def get_order(
    session: AsyncSession,
    register_customer: dict[str, Any],
    order: Order,
) -> Order | None:
    order = await crud_common.get_db_item_by_id(
        session=session,
        id_item=order.id,
        model_item=Order,
    )
    return order


@pytest.fixture
async def create_order(
    session: AsyncSession,
    get_order: Order | None,
    order: Order,
) -> Order:

    if get_order:
        return get_order

    create_order_data = CreateOrder(
        user_id=order.user_id,
        subject_name=order.subject_name,
        description=order.description,
        is_active=order.is_active,
    )

    order = await crud_common.create_db_item(
        session=session, model_db=Order, data=create_order_data
    )

    return order


@pytest.fixture
async def delete_order(
    session: AsyncSession,
    get_order: Order | None,
):
    if not get_order:
        return

    await crud_common.delete_db_item(
        session=session,
        delete_item=get_order,
    )
