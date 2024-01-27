from fastapi import HTTPException, status, Depends

from .views import fastapi_users
from core.models import User


async def checking_tutor(
        user: User = Depends(fastapi_users.current_user())
) -> User | HTTPException:
    """Checking if the user is a tutor"""
    # check constant:
    # Role.tutor
    if user.role == 'tutor':
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
    )


class CurrentUser:

    def get_superuser(self) -> User:
         return fastapi_users.current_user(
             active=True,
             superuser=True,
         )

    def get_current_user(self) -> User:
        return fastapi_users.current_user()

    def get_user(self, require_superuser: bool = False) -> User:
        """
        Depends(current_user.get_user())
        Depends(current_user.get_user(require_superuser=True))
        """
        return fastapi_users.current_user(
             active=True,
             superuser=require_superuser,
        )


current_user = CurrentUser()