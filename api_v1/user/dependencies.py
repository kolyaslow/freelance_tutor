from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from api_v1.user import fastapi_users


if TYPE_CHECKING:
    from core.models import User

class CurrentUser():

    def get_superuser(self) -> User:
         return fastapi_users.current_user(
             active=True,
             superuser=True,
         )

    def get_current_user(self) -> User:
        return fastapi_users.current_user()

    def get_tutor(self) -> User | HTTPException:
        user = fastapi_users.current_user()

        if user.role == 'tutor':
            return user

        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )

current_user = CurrentUser()