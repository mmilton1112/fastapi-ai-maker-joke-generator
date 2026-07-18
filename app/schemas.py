from pydantic import BaseModel, Field


class JokeResponse(BaseModel):
    id: str
    joke: str
    category: str
    keywords: str
    date_added: str
    rating: int


class KeywordRequest(BaseModel):
    keyword: str = Field(..., min_length=1, description="Keyword to search jokes by")
    count: int = Field(default=1, ge=1, le=10, description="Number of jokes to return")


class JokesListResponse(BaseModel):
    jokes: list[JokeResponse]
    count: int
