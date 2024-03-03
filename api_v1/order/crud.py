from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.order.schemas import OrderingWithCustomer
from core.models import Order, Subject, User


async def get_all_orders(
    session: AsyncSession,
    user: User,
) -> list[Order]:
    stmt = select(Order).where(Order.user_id == user.id)
    orders = await session.scalars(stmt)
    return list(orders)


async def getting_orders_for_tutor(
    session: AsyncSession,
    user_id: int,
    page: int,
    size: int,
) -> list[OrderingWithCustomer]:
    """Получение заказов, которые может взять рпетитор"""
    offset_min = page * size
    offset_max = (page + 1) * size

    stmt = (
        select(Order.description, Order.subject_name, Order.id)
        .join(User.subjects)
        .join(Subject.orders)
        .where(User.id == user_id)
        .order_by(desc(Order.id))
        .offset(offset_min)
        .limit(offset_max - offset_min + 1)
    )

    result = await session.execute(stmt)
    return list(result)
