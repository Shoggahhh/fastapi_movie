from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from starlette.testclient import TestClient

from api.api_v1.movie.crud import storage
from main import app
from schemas.movie import DESCRIPTION_MAX_LENGTH, Movie
from testing.conftest import create_movie


class TestUpdatePartial:

    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie]:
        slug, description = request.param
        movie = create_movie(
            slug=slug,
            description=description,
        )
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param(
                ("foo", "some description"),
                "",
                id="some-descriptiom-to-no-description",
            ),
            pytest.param(
                ("bar", ""),
                "some description",
                id="no-description-to-some-description",
            ),
            pytest.param(
                ("max-to-min", "a" * DESCRIPTION_MAX_LENGTH),
                "",
                id="max-description-to-no-description",
            ),
            pytest.param(
                ("min-to-max", ""),
                "a" * DESCRIPTION_MAX_LENGTH,
                id="no-description-to-max-description",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self,
        movie: Movie,
        new_description: str,
        auth_client: TestClient,
    ) -> None:
        url = app.url_path_for(
            "update_movie_details_partial",
            slug=movie.slug,
        )
        response = auth_client.patch(
            url,
            json={"description": new_description},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_db = storage.get_by_slug(movie.slug)
        assert movie_db
        assert movie_db.description == new_description
