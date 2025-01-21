from enum import Enum


class SortOrder(str, Enum):
    ASC = "oldest"
    DESC = "newest"
