from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, AnyHttpUrl
from random import randint


class MovieBase(BaseModel):
    movie_id: int = randint(3, 10)
    name: str
    description: str
    rating: str
    age_rating: str
    url: AnyHttpUrl


class MovieCreate(BaseModel):
    """
    Model for create Movie model
    """

    name: Annotated[str, Len(min_length=1, max_length=59)]
    description: Annotated[str, Len(min_length=5, max_length=100)]
    rating: Annotated[str, Len(min_length=1, max_length=2)]
    age_rating: Annotated[str, Len(min_length=2, max_length=3)]
    url: AnyHttpUrl


class Movie(MovieBase):
    """
    Model of Movie
    """
