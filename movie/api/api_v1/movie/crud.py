from pydantic import BaseModel, ValidationError

from movie.schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MoviePartialUpdate,
)
from core.config import MOVIE_STORAGE_DIR

import logging

"""
Create
Reade
Update
Delete
"""

log = logging.getLogger(__file__)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self):
        MOVIE_STORAGE_DIR.write_text(self.model_dump_json(indent=2))
        log.info("Saved movie to storage file")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_DIR.exists():
            log.info("Movie to storage file doesn't exist")
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_DIR.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error")
            return

        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        log.warning("Recovered data from storage file")

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie_in.slug] = movie
        log.info("Created movie %s", movie)
        return movie

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        log.info("Updated movie %s", movie)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        log.info("Updated partial movie %s", movie)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)
        log.info("Deleted movie by slug %s", slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


storage = MovieStorage()
