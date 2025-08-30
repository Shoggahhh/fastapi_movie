from unittest import TestCase

from schemas.movie import Movie, MovieCreate


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
