from fastapi import HTTPException
from starlette import status

from api.api_v1.movie.crud import MOVIES
from schemas.movie import Movie


def prefetch_movie(slug: str):
    movie: Movie | None = next(
        (movie for movie in MOVIES if movie.slug == slug),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie on this id: {slug!r} not found",
    )
