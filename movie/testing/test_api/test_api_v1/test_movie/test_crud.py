import random
import string
from os import getenv
from unittest import TestCase

from api.api_v1.movie.crud import storage
from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate

if getenv("TESTING") != "1":
    msg = "Environment is not ready to testing"
    raise OSError(msg)


class MovieCreateUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = self.create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def create_movie(self) -> Movie:
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
