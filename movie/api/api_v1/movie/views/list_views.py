from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movie.crud import storage
from api.api_v1.movie.dependencies import save_storage_state
from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(save_storage_state)],
)


@router.get("/", response_model=list[MovieRead])
def read_all_movies():
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)
