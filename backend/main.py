# backend/main.py

from datetime import date
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="CinemaThisWeek API")


class Clue(BaseModel):
    order_index: int
    text: str


class TodayGameResponse(BaseModel):
    game_date: date
    movie_slug: str
    total_clues: int
    first_clue: Clue


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/today-game", response_model=TodayGameResponse)
def get_today_game():

    fake_clues: List[Clue] = [
        Clue(
            order_index=1,
            text="A quiet coastal town is disrupted by an unusual threat.",
        ),
        Clue(
            order_index=2,
            text="The danger lurks beneath the surface, unseen but deadly.",
        ),
        Clue(
            order_index=3,
            text="A small group of locals and outsiders try to warn everyone.",
        ),
        Clue(
            order_index=4,
            text="An iconic poster features a swimmer.",
        ),
    ]

    first_clue = fake_clues[0]

    # This slug is what the frontend will use to identify the movie.
    # In the real system it might be something like an internal ID or hash.
    return TodayGameResponse(
        game_date=date.today(),
        movie_slug="daily-movie-stub",
        total_clues=len(fake_clues),
        first_clue=first_clue,
    )
