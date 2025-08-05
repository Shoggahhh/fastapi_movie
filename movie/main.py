from fastapi import FastAPI, Request
from api import router as api_router
from api.redirect_views import router as redirect_router
import logging
from movie.core import config

app = FastAPI()

app.include_router(redirect_router)
app.include_router(api_router)

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)


@app.get("/")
def read_root(request: Request):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {"docs": str(docs_url)}
