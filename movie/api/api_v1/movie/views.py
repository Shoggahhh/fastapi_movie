from fastapi import APIRouter, status, Depends

from api.api_v1.movie.dependecies import prefetch_movie
from api.api_v1.movie.crud import MOVIES
from movie.schemas.movie import Movie, MovieCreate
from typing import Annotated

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
def create_movie(movie_create: MovieCreate) -> Movie:
    return Movie(**movie_create.model_dump())


@router.get("/movie/{movie_id}", response_model=Movie)
def get_movie_from_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie
