from fastapi_users import FastAPIUsers

from api_v1.user.config import auth_backend, get_user_manager
from core.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
