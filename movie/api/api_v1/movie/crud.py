import json

from pydantic import BaseModel, AnyHttpUrl, ValidationError

from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)
from core.config import MOVIE_STORAGE_DIR


"""
Create
Reade
Update
Delete
"""


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self):
        MOVIE_STORAGE_DIR.write_text(self.model_dump_json(indent=2))

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_DIR.exists():
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_DIR.read_text())

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie_in.slug] = movie
        self.save_state()
        return movie

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_state()
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        self.save_state()

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


try:
    storage = MovieStorage.from_state()
except ValidationError:
    storage = MovieStorage()
    storage.save_state()

# storage = MovieStorage()
#
#
# storage.create(
#     MovieCreate(
#         slug="mtrx",
#         name="Matrix",
#         description="some desc",
#         rating="9.5",
#         age_rating="18+",
#         url=AnyHttpUrl("https://www.kinopoisk.ru/film/301/"),
#     )
# )
#
# storage.create(
#     MovieCreate(
#         slug="lotr",
#         name="Lord of the rings",
#         description="some desc",
#         rating="10",
#         age_rating="18+",
#         url=AnyHttpUrl("https://www.kinopoisk.ru/film/328/"),
#     )
# )
