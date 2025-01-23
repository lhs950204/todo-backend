from enum import Enum

from pydantic import BaseModel


class SortOrder(str, Enum):
    ASC = "oldest"
    DESC = "newest"


class CursorPaginationBase(BaseModel):
    next_cursor: int | None
    total_count: int
