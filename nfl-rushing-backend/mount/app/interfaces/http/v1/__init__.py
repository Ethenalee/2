from fastapi import APIRouter
from . import rushing


router = APIRouter()
router.include_router(rushing.router)
