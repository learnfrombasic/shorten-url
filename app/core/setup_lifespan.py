from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common import setup_logger
from app.core.config import settings
from app.core.db import init_mongodb

logger = setup_logger("Core")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Welcome to {settings.APP}")
    await init_mongodb()
    
    yield

    logger.info("Shutting down the server")
