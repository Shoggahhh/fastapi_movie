from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import AnyHttpUrl, BaseModel

DESCRIPTION_MAX_LENGTH = 200

NameString = Annotated[str, Len(min_length=1, max_length=60)]
DescriptionString = Annotated[str, MaxLen(DESCRIPTION_MAX_LENGTH)]
RatingString = Annotated[str, Len(min_length=1, max_length=3)]
AgeRatingString = Annotated[str, Len(min_length=2, max_length=3)]
SubtitlesString = Annotated[str, Len(max_length=3)]


class MovieBase(BaseModel):
    name: NameString
    description: DescriptionString
    rating: RatingString
    age_rating: AgeRatingString
    subtitles: SubtitlesString
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

    subtitles: SubtitlesString = "ENG"


class MoviePartialUpdate(BaseModel):
    """
    Model for partial update
    """

    name: NameString | None = None
    description: DescriptionString | None = None
    rating: RatingString | None = None
    age_rating: AgeRatingString | None = None
    subtitles: SubtitlesString | None = None
    url: AnyHttpUrl | None = None


class MovieRead(MovieBase):
    """
    Model to read data movie
    """

    slug: str


class Movie(MovieBase):
    """
    Model of Movie
    """

    slug: str
    notes: str = "qwe"
