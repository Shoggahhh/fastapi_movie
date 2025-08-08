import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Header,
    status,
)
from fastapi.params import Depends

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from api.api_v1.movie.crud import storage
from core.config import API_TOKENS
from schemas.movie import Movie


log = logging.getLogger(__file__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **static API token** from developer portal. [Read more](#)",
    auto_error=False,
)


def prefetch_movie(slug: str):
    movie: Movie | None = storage.get_by_slug(slug=slug)

    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie on this slug: {slug!r} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):
    log.info("incoming %r request", request.method)
    yield
    if request.method in UNSAFE_METHODS:
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    log.info("Api token: %s", api_token)
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )
    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
