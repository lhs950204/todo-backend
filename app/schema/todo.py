from typing import Sequence

from pydantic import BaseModel, Field

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


class TodoResponse(BaseModel):
    id: int
    title: str
    done: bool
    link_url: str | None = None
    file_url: str | None = None
    user_id: int
    goal_id: int
    created_at: str
    updated_at: str
    note_id: int | None = None


class TodoList(CursorPaginationBase):
    todos: Sequence[TodoResponse]
