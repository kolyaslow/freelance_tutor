from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user_by_email(
    session: AsyncSession,
    email: str,
):
    stmt = select(User).where(User.email == email)
    user = await session.scalar(stmt)
    return user
