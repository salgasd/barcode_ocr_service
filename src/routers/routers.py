from fastapi import APIRouter

from src.routers.v1.api import model_router

v1_router = APIRouter(tags=["v1"], prefix="/api/v1")

v1_router.include_router(model_router)
