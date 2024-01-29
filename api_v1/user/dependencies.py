from fastapi import HTTPException, status, Depends

from .views import fastapi_users
from core.models import User
from .schemas import Role


async def checking_tutor(
        user: User = Depends(fastapi_users.current_user())
) -> User | HTTPException:
    """Checking if the user is a tutor"""
    if user.role == Role.tutor:
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



current_user = CurrentUser()