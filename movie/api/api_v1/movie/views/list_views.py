from fastapi import (
    APIRouter,
    status,
    BackgroundTasks,
)

from api.api_v1.movie.crud import storage
from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(prefix="/movies", tags=["Movies"])


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
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_state)
    return storage.create(movie_create)
