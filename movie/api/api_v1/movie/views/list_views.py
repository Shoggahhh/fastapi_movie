from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.movie.crud import storage
from api.api_v1.movie.dependencies import (
    save_storage_state,
    # api_token_required_for_unsafe_methods,
    user_basic_auth_required,
)
from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_storage_state),
        Depends(user_basic_auth_required),
        # Depends(api_token_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
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
