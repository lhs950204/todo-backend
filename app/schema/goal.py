from typing import Sequence

from pydantic import BaseModel

from app.models.goal import Goal
from app.schema.common import CursorPaginationBase


class GoalCreate(BaseModel):
    title: str


class GoalUpdate(GoalCreate):
    title: str


class GoalList(CursorPaginationBase):
    goals: Sequence[Goal]
