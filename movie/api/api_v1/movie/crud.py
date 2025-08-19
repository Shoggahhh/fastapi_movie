from pydantic import BaseModel
from redis import Redis

from core import config
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

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIE,
    decode_responses=True,
)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExists(MovieBaseError):
    """
    Raised in movie creation if such slug is already exists.
    """


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_DIR.exists():
            log.info("Movie to storage file doesn't exist")
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_DIR.read_text())

    def get(self) -> list[Movie]:
        result = [
            Movie.model_validate_json(value)
            for value in redis.hvals(config.REDIS_MOVIES_HASH_NAME)
        ]
        return result

    def get_by_slug(self, slug: str) -> Movie | None:
        result = redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        )
        if result:
            return Movie.model_validate_json(result)
        return None

    def exists(self, slug) -> bool:
        return redis.hexists(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        )

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.save_movie(movie)
        log.info("Created movie %s", movie)
        return movie

    def create_or_raise_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)
        raise MovieAlreadyExists(movie_in.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate):
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        log.info("Updated movie %s", movie)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate):
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        log.info("Updated partial movie %s", movie)
        return movie

    def save_movie(self, movie: Movie):
        redis.hset(
            config.REDIS_MOVIES_HASH_NAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(
            config.REDIS_MOVIES_HASH_NAME,
            slug,
        )
        log.info("Deleted movie by slug %s", slug)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)


storage = MovieStorage()
