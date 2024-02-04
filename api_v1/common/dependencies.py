from typing import Type

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user.views import fastapi_users
from core.models import User, Base
from core.db_helper import db_helper
from api_v1.user.schemas import Role
from . import crud as crud_common



class UserRights:

    async def __checking_role(
            self,
            role: Role,
            user: User,
    ) -> User:
        if user.role == role:
            return user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    async def checking_tutor(
            self,
            user: User = Depends(fastapi_users.current_user())
    ) -> User:
        """Проверка является ли текщий пользователей репетитором"""
        return await self.__checking_role(Role.tutor, user=user)

    async def checking_customer(
            self,
            user: User = Depends(fastapi_users.current_user())
    ) -> User:
        """Проверка является ли текщий пользователей репетитором"""
        return await self.__checking_role(Role.customer, user=user)

    async def checking_superuser(
            self,
            user: User = Depends(
                fastapi_users.current_user(
                    active=True,
                    superuser=True,
                )
            )
    ) -> User:
         return user

    async def checking_current_user(
        self,
        user: User = Depends(fastapi_users.current_user())
    ) -> User:
        return user


user_rights = UserRights()


async def get_item_db_by_id(
        item_id: int | str,
        model_db: Type[Base],
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    item_db = await crud_common.get_db_item_by_id(
        session=session,
        id_item=item_id,
        model_item=model_db,
    )

    if item_db:
        return item_db

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Незвозможно получить объект по его id'
    )

