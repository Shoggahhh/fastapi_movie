from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.movie.crud import storage
from api.api_v1.movie.dependencies import prefetch_movie
from schemas.movie import Movie, MovieUpdate, MoviePartialUpdate

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

MovieBySlug = Annotated[
    Movie,
    Depends(prefetch_movie),
]


@router.get("/", response_model=Movie)
def read_movie_from_slug(movie: MovieBySlug) -> Movie:
    return movie


@router.put("/", response_model=Movie)
def update_movie_details(movie: MovieBySlug, movie_in: MovieUpdate) -> Movie:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch("/", response_model=Movie)
def update_movie_details_partial(
    movie: MovieBySlug, movie_in: MoviePartialUpdate
) -> Movie:
    return storage.update_partial(
        movie=movie,
        movie_in=movie_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(movie: MovieBySlug) -> None:
    storage.delete(movie=movie)
