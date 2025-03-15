from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common import setup_logger
from app.core.config import settings

logger = setup_logger("Core")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Welcome to {settings.APP}")

    yield

    logger.info("Shutting down the server")
