import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movie.crud import storage
from main import app
from schemas.movie import Movie
from testing.conftest import create_movie


@pytest.fixture(
    params=[
        "some-slug",
        "slug",
        pytest.param("abc", id="minimal-slug"),
        pytest.param("qwertyabcd", id="max-slug"),
    ],
)
def movie(request: SubRequest) -> Movie:
    return create_movie(request.param)


@pytest.mark.apitest
def test_delete_movie(
    movie: Movie,
    auth_client: TestClient,
) -> None:
    url = app.url_path_for(
        "delete_movie",
        slug=movie.slug,
    )
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
