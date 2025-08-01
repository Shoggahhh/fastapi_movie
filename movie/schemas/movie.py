from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, AnyHttpUrl


class MovieBase(BaseModel):
    name: Annotated[str, Len(min_length=1, max_length=60)]
    description: Annotated[str, Len(min_length=5, max_length=100)]
    rating: Annotated[str, Len(min_length=1, max_length=3)]
    age_rating: Annotated[str, Len(min_length=2, max_length=3)]
    subtitles: Annotated[str, Len(max_length=3)] = "ENG"
    url: AnyHttpUrl


class MovieCreate(MovieBase):
    """
    Model for create Movie model
    """

    # noinspection PyTypeHints
    slug: Annotated[str, Len(min_length=3, max_length=10)]


class MovieUpdate(MovieBase):
    """
    Model for update Movie model
    """
    name: Annotated[str, Len(min_length=1, max_length=60)]
    description: Annotated[str, Len(min_length=5, max_length=100)]
    rating: Annotated[str, Len(min_length=1, max_length=3)]
    age_rating: Annotated[str, Len(min_length=2, max_length=3)]
    subtitles: Annotated[str, Len(max_length=3)]
    url: AnyHttpUrl


class Movie(MovieBase):
    """
    Model of Movie
    """

    slug: str
