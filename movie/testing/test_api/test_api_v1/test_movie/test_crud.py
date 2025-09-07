import random
import string
from typing import ClassVar
from unittest import TestCase

import pytest

from api.api_v1.movie.crud import (
    MovieAlreadyExistsError,
    storage,
)
from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        name="some name",
        description="some description",
        rating="100",
        age_rating="18+",
        subtitles="ENG",
        url="https://example.com",
    )
    return storage.create(movie_in)


class MovieCreateUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        movie_update = MovieUpdate(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description
        movie_update.description *= 2
        update_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )
        self.assertNotEqual(
            source_description,
            update_movie.description,
        )
        self.assertEqual(
            movie_update.description,
            update_movie.description,
        )

    def test_update_partial(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_partial_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )
        self.assertNotEqual(
            source_description,
            updated_partial_movie.description,
        )
        self.assertEqual(
            movie_partial_update.description,
            updated_partial_movie.description,
        )


class MovieStorageGetMovieTestCase(TestCase):
    MOVIE_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIE_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_all(self) -> None:
        movies = storage.get()
        expected_slugs = {movie.slug for movie in self.movies}
        slugs = {movie.slug for movie in movies}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(
            expected_diff,
            diff,
        )

    def test_get_movie_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )


def test_create_or_raise_if_exist() -> None:
    existing_movie = create_movie()
    movie_create = MovieCreate(**existing_movie.model_dump())
    with pytest.raises(
        MovieAlreadyExistsError,
        match=movie_create.slug,
    ) as exc_info:
        storage.create_or_raises_if_exists(movie_create)

    assert exc_info.value.args[0] == movie_create.slug
