from fastapi import FastAPI, Request, Response
from api import router as api_router
from api.redirect_views import router as redirect_router
import logging

from app_lifespan import lifespan
from core import config

app = FastAPI(
    title="Movie",
    lifespan=lifespan,
)

app.include_router(redirect_router)
app.include_router(api_router)

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)


@app.get("/")
def read_root(request: Request) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {"docs": str(docs_url)}
