from fastapi import APIRouter, status, Depends

from api.api_v1.movie.dependencies import prefetch_movie
from api.api_v1.movie.crud import storage
from movie.schemas.movie import Movie, MovieCreate
from typing import Annotated

import random

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[Movie])
def get_all_movies():
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate) -> Movie:
    return storage.create(movie_create)


@router.get("/movie/{slug}", response_model=Movie)
def get_movie_from_slug(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> Movie:
    return movie


@router.delete(
    "movie/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
) -> None:
    storage.delete(movie=movie)
