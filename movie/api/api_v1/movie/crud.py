from pydantic import BaseModel, AnyHttpUrl

from movie.schemas.movie import (
    Movie,
    MovieCreate,
)


"""
Create
Reade
Update
Delete
"""


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: Movie) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie_in.slug] = movie
        return movie


storage = MovieStorage()


storage.create(
    Movie(
        slug="mtrx",
        name="Matrix",
        description="some desc",
        rating="9.5",
        age_rating="18+",
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/301/"),
    )
)

storage.create(
    Movie(
        slug="lotr",
        name="Lord of the rings",
        description="some desc",
        rating="10",
        age_rating="18+",
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/328/"),
    )
)
