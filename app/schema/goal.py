from typing import Sequence

from pydantic import BaseModel

from app.models.goal import Goal


class GoalCreate(BaseModel):
    title: str


class GoalUpdate(GoalCreate):
    title: str


class GoalList(BaseModel):
    next_cursor: int | None
    total_count: int
    goals: Sequence[Goal]
