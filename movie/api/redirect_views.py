from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated
from api.api_v1.movie.dependencies import prefetch_movie

from schemas.movie import Movie

router = APIRouter(prefix="/r", tags=["Redirect"])


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_on_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
):
    return RedirectResponse(
        url=str(movie.url),
    )
