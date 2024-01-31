from typing import Type

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


async def create_db_item(
        session: AsyncSession,
        model_db: Type[Base],
        data: BaseModel
):
    item = model_db(**data.model_dump())
    session.add(item)
    await session.commit()
    return item