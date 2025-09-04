import logging

from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from api.redirect_views import router as redirect_router
from app_lifespan import lifespan
from core import config

app = FastAPI(
    title="Movie",
    lifespan=lifespan,
)

app.include_router(redirect_router)
app.include_router(api_router)
app.include_router(main_router)

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
