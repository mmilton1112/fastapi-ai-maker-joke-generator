from __future__ import annotations

import asyncio

from fastapi import FastAPI, HTTPException, Query

from app.schemas import JokeResponse, JokesListResponse, KeywordRequest
from app.services import fetch_jokes_by_keyword, fetch_random_jokes

app = FastAPI(
    title="Joke Generator API",
    description="Get random jokes or search jokes by keyword (sync and async).",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/jokes/random/sync", response_model=JokesListResponse)
def get_random_joke_sync(
    count: int = Query(default=1, ge=1, le=10),
) -> JokesListResponse:
    jokes = fetch_random_jokes(count=count)
    return JokesListResponse(jokes=jokes, count=len(jokes))


@app.get("/jokes/random/async", response_model=JokesListResponse)
async def get_random_joke_async(
    count: int = Query(default=1, ge=1, le=10),
) -> JokesListResponse:
    jokes = await asyncio.to_thread(fetch_random_jokes, count)
    return JokesListResponse(jokes=jokes, count=len(jokes))


@app.post("/jokes/keyword/sync", response_model=JokesListResponse)
def search_jokes_by_keyword_sync(request: KeywordRequest) -> JokesListResponse:
    jokes = fetch_jokes_by_keyword(keyword=request.keyword, count=request.count)
    if not jokes:
        raise HTTPException(
            status_code=404,
            detail=f"No jokes found for keyword: {request.keyword}",
        )
    return JokesListResponse(jokes=jokes, count=len(jokes))


@app.post("/jokes/keyword/async", response_model=JokesListResponse)
async def search_jokes_by_keyword_async(request: KeywordRequest) -> JokesListResponse:
    jokes = await asyncio.to_thread(
        fetch_jokes_by_keyword,
        request.keyword,
        request.count,
    )
    if not jokes:
        raise HTTPException(
            status_code=404,
            detail=f"No jokes found for keyword: {request.keyword}",
        )
    return JokesListResponse(jokes=jokes, count=len(jokes))
