import random
import string

from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movie import MovieCreate


def test_create_movie(auth_client: TestClient) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=5,
            ),
        ),
        name="some name",
        description="some description",
        rating="100",
        age_rating="18+",
        subtitles="ENG",
        url="https://example.com",
    )
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(
        url=url,
        json=data,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    received_value = MovieCreate(**response_data)
    assert received_value == movie_create, response_data
