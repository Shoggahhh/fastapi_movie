import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.movie.crud import storage
from schemas.movie import Movie


log = logging.getLogger(__file__)


def prefetch_movie(slug: str):
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie on this slug: {slug!r} not found",
    )


def save_storage_state(background_tasks: BackgroundTasks):
    yield
    log.info("Add background task to save storage")
    background_tasks.add_task(storage.save_state)
