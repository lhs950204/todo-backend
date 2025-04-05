from typing import Sequence

from pydantic import BaseModel, Field

from app.models.goal import GoalBase
from app.models.note import NoteBase
from app.models.todo import TodoBase
from app.models.user import UserBase
from app.schema.common import CursorPaginationBase


class NoteCreate(BaseModel):
    title: str
    content: str
    link_url: str
    goal_id: int
    todo_id: int


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    link_url: str | None = Field(None, alias="linkUrl")


class NoteResponse(NoteBase):
    todo: TodoBase | None = None
    goal: GoalBase | None = None
    user: UserBase | None = None


class NoteList(CursorPaginationBase):
    notes: Sequence[NoteResponse]
