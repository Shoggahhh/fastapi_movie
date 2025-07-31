from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.movie.crud import storage
from api.api_v1.movie.dependencies import prefetch_movie
from schemas.movie import Movie

router = APIRouter(
    prefix="/movie/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie on this 'slug' not found",
                    },
                },
            },
        },
    },
)


@router.get("/", response_model=Movie)
def read_movie_from_slug(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie:
    return movie


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> None:
    storage.delete(movie=movie)
