from unittest import TestCase

from schemas.movie import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


class MovieTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some slug",
            name="some name",
            description="some description",
            rating="100",
            age_rating="18+",
            subtitles="ENG",
            url="https://example.com",
        )
        movie = Movie(
            **movie_in.model_dump(),
        )

        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.name, movie.name)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.rating, movie.rating)
        self.assertEqual(movie_in.age_rating, movie.age_rating)
        self.assertEqual(movie_in.subtitles, movie.subtitles)
        self.assertEqual(movie_in.url, movie.url)

    def test_movie_can_be_update_from_update_schema(self) -> None:
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
            name="new name",
            description="new description",
            rating="9.5",
            age_rating="16+",
            subtitles="RU",
            url="https://new-example.com",
        )

        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        self.assertEqual(movie_in.name, movie.name)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.rating, movie.rating)
        self.assertEqual(movie_in.age_rating, movie.age_rating)
        self.assertEqual(movie_in.subtitles, movie.subtitles)
        self.assertEqual(movie_in.url, movie.url)

    def test_movie_can_be_from_update_partial_schema(self) -> None:
        movie_in = MoviePartialUpdate(
            description="another some description",
        )
        movie = Movie(
            slug="some slug",
            name="new name",
            description="new description",
            rating="9.5",
            age_rating="16+",
            subtitles="RU",
            url="https://new-example.com",
        )
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.assertEqual(movie.name, movie.name)
        self.assertEqual(movie.description, movie.description)
        self.assertEqual(movie.rating, movie.rating)
        self.assertEqual(movie.age_rating, movie.age_rating)
        self.assertEqual(movie.subtitles, movie.subtitles)
        self.assertEqual(movie.url, movie.url)
