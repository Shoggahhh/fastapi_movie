from pydantic import BaseModel, AnyHttpUrl


class MovieBase(BaseModel):
    movie_id: int
    name: str
    description: str
    rating: str
    age_rating: str
    url: AnyHttpUrl


class Movie(MovieBase):
    """
    Model of Film
    """
