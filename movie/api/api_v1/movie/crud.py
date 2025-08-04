from pydantic import BaseModel, AnyHttpUrl

from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
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

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie_in.slug] = movie
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()


storage.create(
    MovieCreate(
        slug="mtrx",
        name="Matrix",
        description="some desc",
        rating="9.5",
        age_rating="18+",
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/301/"),
    )
)

storage.create(
    MovieCreate(
        slug="lotr",
        name="Lord of the rings",
        description="some desc",
        rating="10",
        age_rating="18+",
        url=AnyHttpUrl("https://www.kinopoisk.ru/film/328/"),
    )
)
