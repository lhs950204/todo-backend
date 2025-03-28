from typing import Sequence

from pydantic import BaseModel, Field

from app.models.todo import Todo
from app.schema.common import CursorPaginationBase


class TodoCreate(BaseModel):
    title: str
    file_url: str | None = Field(alias="fileUrl", default=None)
    link_url: str | None = Field(alias="linkUrl", default=None)
    goal_id: int = Field(alias="goalId")


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
    file_url: str | None = Field(None, alias="fileUrl")
    link_url: str | None = Field(None, alias="linkUrl")
    goal_id: int | None = Field(None, alias="goalId")


class TodoList(CursorPaginationBase):
    todos: Sequence[Todo]
