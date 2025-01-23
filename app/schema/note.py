from typing import Sequence

from pydantic import BaseModel

from app.models.note import Note
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
    link_url: str | None = None


class NoteList(CursorPaginationBase):
    notes: Sequence[Note]
