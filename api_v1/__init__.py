from .user.views import router as user_router
from fastapi import APIRouter
from .subject.views import router as subject_router

router = APIRouter()
router.include_router(router=user_router)
router.include_router(router=subject_router, prefix='/subject')

