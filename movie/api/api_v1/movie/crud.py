import logging
from collections.abc import Iterable
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core import config
from schemas.movie import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)

"""
Create
Reade
Update
Delete
"""

log = logging.getLogger(__name__)


class MovieBaseError(Exception):
    """
    Base exception for movie CRUD actions.
    """


class MovieAlreadyExistsError(MovieBaseError):
    """
    Raised in movie creation if such slug is already exists.
    """


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIE,
    decode_responses=True,
)


class MovieStorage(BaseModel):

    def get(self) -> list[Movie]:
        return [
            Movie.model_validate_json(value)
            for value in cast(Iterable[str], redis.hvals(config.REDIS_MOVIES_HASH_NAME))
        ]

    def get_by_slug(self, slug: str) -> Movie | None:
        data = redis.hget(
            name=config.REDIS_MOVIES_HASH_NAME,
            key=slug,
        )
        if data:
            assert isinstance(data, str)
            return Movie.model_validate_json(data)
        return None

    def exists(self, slug: str) -> bool:
        return cast(
            bool,
            redis.hexists(name=config.REDIS_MOVIES_HASH_NAME, key=slug),
        )

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.save_movie(movie)
        log.info("Created movie %s", movie)
        return movie

    def create_or_raises_if_exists(self, movie_in: MovieCreate) -> Movie:
        if not self.exists(movie_in.slug):
            return self.create(movie_in)

        raise MovieAlreadyExistsError(movie_in.slug)

    def update(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        self.save_movie(movie)
        log.info("Updated movie %s", movie)
        return movie

    def update_partial(self, movie: Movie, movie_in: MoviePartialUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        self.save_movie(movie)
        log.info("Updated partial movie %s", movie)
        return movie

    def save_movie(self, movie: Movie) -> None:
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
