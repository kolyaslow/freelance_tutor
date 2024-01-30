from fastapi import HTTPException, status, Depends

from api_v1.user.views import fastapi_users
from core.models import User
from api_v1.user.schemas import Role



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