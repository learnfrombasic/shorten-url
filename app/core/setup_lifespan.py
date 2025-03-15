from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.common import setup_logger


logger = setup_logger("Core")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Welcome to {settings.APP}")
    
    yield

    logger.info("Shutting down the server")
