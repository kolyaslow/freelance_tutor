from .user.views import router as user_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(router=user_router)

