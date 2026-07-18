from __future__ import annotations

import random
from pathlib import Path

from joke_generator import (
    DEFAULT_JOKES_FILE,
    Joke,
    find_jokes_by_keyword,
    get_random_joke,
    load_jokes,
)

from app.schemas import JokeResponse


def joke_to_response(joke: Joke) -> JokeResponse:
    return JokeResponse(
        id=joke.id,
        joke=joke.text,
        category=joke.category,
        keywords=joke.keywords,
        date_added=joke.date_added,
        rating=int(joke.rating),
    )


def fetch_random_jokes(count: int = 1, jokes_file: Path = DEFAULT_JOKES_FILE) -> list[JokeResponse]:
    jokes = load_jokes(jokes_file)
    selected = [get_random_joke(jokes) for _ in range(count)]
    return [joke_to_response(joke) for joke in selected]


def fetch_jokes_by_keyword(
    keyword: str,
    count: int = 1,
    jokes_file: Path = DEFAULT_JOKES_FILE,
) -> list[JokeResponse]:
    jokes = load_jokes(jokes_file)
    matches = find_jokes_by_keyword(jokes, keyword)
    if not matches:
        return []

    selected = random.sample(matches, k=min(count, len(matches)))
    return [joke_to_response(joke) for joke in selected]
