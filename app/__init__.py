from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.setup_lifespan import lifespan

app = FastAPI(
    title="Oryza AI FastAPI Face Recogition's Service",
    docs_url="/",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
