from fastapi import APIRouter

from app.api.routers import shorten_url_router

api_router = APIRouter()

api_router.include_router(shorten_url_router.router, tags=["SHORTEN_URL"])
