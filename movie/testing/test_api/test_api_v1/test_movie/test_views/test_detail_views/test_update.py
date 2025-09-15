from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from api.api_v1.movie.crud import storage
from main import app
from schemas.movie import DESCRIPTION_MAX_LENGTH, Movie
from testing.conftest import create_movie_random_slug


class TestUpdate:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        name, description = request.param
        movie = create_movie_random_slug(
            name=name,
            description=description,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_name, new_description",
        [
            pytest.param(
                ("a", "b"),
                "some name",
                "some description",
                id="min-name-and-description-to-some-name-and-description",
            ),
            pytest.param(
                ("a", "b"),
                "a" * 60,
                "a" * DESCRIPTION_MAX_LENGTH,
                id="max-name-and-description-to-some-name-and-description",
            ),
            pytest.param(
                ("a", "b"),
                "some name",
                "some description",
                id="no-name-and_description-to-some-name-and-description",
            ),
            pytest.param(
                ("some name", "some description"),
                "a",
                "b",
                id="some-name-and-description-to-no-name-and-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        new_name: str,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_movie_details",
            slug=movie.slug,
        )
        updated_movie = movie.model_copy(
            update={
                "name": new_name,
                "description": new_description,
            },
        )
        response = auth_client.put(
            url,
            json=updated_movie.model_dump(mode="json"),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.name == new_name
        assert movie_db.description == new_description
