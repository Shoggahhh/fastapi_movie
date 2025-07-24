from fastapi import APIRouter
from fastapi.params import Depends

from api.api_v1.movie.dependecies import prefetch_movie
from api.api_v1.movie.crud import MOVIES
from movie.schemas.movie import Movie
from typing import Annotated

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=list[Movie])
def get_all_movies():
    return MOVIES


@router.get("/movie/{movie_id}", response_model=Movie)
def get_movie_from_id(movie: Annotated[Movie, Depends(prefetch_movie)]) -> Movie:
    return movie
