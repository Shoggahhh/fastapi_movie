import random
import string
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.movie import Movie, MovieCreate
from testing.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


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


def test_create_or_already_exist(
    auth_client: TestClient,
    movie: Movie,
) -> None:
    url = app.url_path_for("create_movie")
    movie_create = MovieCreate(**movie.model_dump())
    data: dict[str, str] = movie_create.model_dump(mode="json")
    response = auth_client.post(
        url=url,
        json=data,
    )
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug={movie_create.slug!r} is already exists"
    assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="string-too-short"),
            pytest.param(("qwertyabcde", "string_too_long"), id="string-too-long"),
        ],
    )
    def movie_create_values(self, request: SubRequest) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data: dict[str, str] = build.model_dump(mode="json")
        slug, err = request.param
        data["slug"] = slug
        return data, err

    def test_invalid_slug(
        self,
        auth_client: TestClient,
        movie_create_values: tuple[dict[str, Any], str],
    ) -> None:
        url = app.url_path_for("create_movie")
        create_data, expected_err = movie_create_values
        response = auth_client.post(
            url,
            json=create_data,
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_err, error_detail
