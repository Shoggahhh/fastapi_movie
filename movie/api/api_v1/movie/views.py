from fastapi import APIRouter, status, Form, Depends
from pydantic import AnyHttpUrl

from api.api_v1.movie.dependecies import prefetch_movie
from api.api_v1.movie.crud import MOVIES
from movie.schemas.movie import Movie
from typing import Annotated
from annotated_types import Len

import random

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[Movie])
def get_all_movies():
    return MOVIES


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    name: Annotated[str, Len(min_length=1, max_length=59), Form()],
    description: Annotated[str, Len(min_length=5, max_length=100), Form()],
    rating: Annotated[str, Len(min_length=1, max_length=2), Form()],
    age_rating: Annotated[str, Len(min_length=2, max_length=3), Form()],
    url: Annotated[AnyHttpUrl, Form()],
):
    return Movie(
        movie_id=random.randint(3, 10),
        description=description,
        name=name,
        rating=rating,
        age_rating=age_rating,
        url=url,
    )


@router.get("/movie/{movie_id}", response_model=Movie)
def get_movie_from_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie
