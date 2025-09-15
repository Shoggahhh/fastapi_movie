import random
import string
from collections.abc import Generator
from os import getenv

import pytest

from api.api_v1.movie.crud import storage
from schemas.movie import Movie, MovieCreate


@pytest.fixture(
    scope="session",
    autouse=True,
)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit("Environment is not ready to testing")


def build_movie_create(
    slug: str,
    name: str = "some name",
    description: str = "A movie",
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        name=name,
        description=description,
        rating="100",
        age_rating="18+",
        subtitles="ENG",
        url="https://example.com",
    )


def build_movie_create_random_slug(
    name: str = "some name",
    description: str = "A movie",
) -> MovieCreate:
    return build_movie_create(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        name=name,
        description=description,
    )


def create_movie(
    slug: str,
    name: str = "some name",
    description: str = "A movie",
) -> Movie:
    movie_in = build_movie_create(
        slug=slug,
        name=name,
        description=description,
    )
    return storage.create(movie_in)


def create_movie_random_slug(
    name: str = "some name",
    description: str = "A movie",
) -> Movie:
    movie_in = build_movie_create_random_slug(
        name=name,
        description=description,
    )
    return storage.create(movie_in)


@pytest.fixture
def movie() -> Generator[Movie]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
