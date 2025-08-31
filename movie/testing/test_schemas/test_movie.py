from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


class MovieCreateTestCase(TestCase):
    def test_movie_can_be_created_from_schema(self) -> None:
        movie = Movie(
            slug="some slug",
            name="some name",
            description="some description",
            rating="100",
            age_rating="18+",
            subtitles="ENG",
            url="https://example.com",
        )
        movie_in = MovieCreate(
            **movie.model_dump(),
        )

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.name,
            movie.name,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.rating,
            movie.rating,
        )
        self.assertEqual(
            movie_in.age_rating,
            movie.age_rating,
        )
        self.assertEqual(
            movie_in.subtitles,
            movie.subtitles,
        )
        self.assertEqual(
            movie_in.url,
            movie.url,
        )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_update_from_schema(self) -> None:
        movie = Movie(
            slug="some slug",
            name="some name",
            description="some description",
            rating="100",
            age_rating="18+",
            subtitles="ENG",
            url="https://example.com",
        )
        movie_in = MovieUpdate(
            name="new some name",
            description="new some description",
            rating="9.5",
            age_rating="16+",
            subtitles="RU",
            url="https://new-example.com",
        )
        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        self.assertEqual(
            movie_in.name,
            movie.name,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.rating,
            movie.rating,
        )
        self.assertEqual(
            movie_in.age_rating,
            movie.age_rating,
        )
        self.assertEqual(
            movie_in.subtitles,
            movie.subtitles,
        )
        self.assertEqual(
            movie_in.url,
            movie.url,
        )


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_can_be_update_partial_from_schema(self) -> None:
        movie = Movie(
            slug="some slug",
            name="some name",
            description="some description",
            rating="100",
            age_rating="18+",
            subtitles="ENG",
            url="https://example.com",
        )
        movie_in = MoviePartialUpdate(
            description="new some description",
        )

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        self.assertEqual(
            movie.name,
            "some name",
        )
        self.assertEqual(
            movie.description,
            "new some description",
        )
        self.assertEqual(
            movie.rating,
            "100",
        )
        self.assertEqual(
            movie.age_rating,
            "18+",
        )
        self.assertEqual(
            movie.subtitles,
            "ENG",
        )
        self.assertEqual(str(movie.url).rstrip("/"), "https://example.com")
