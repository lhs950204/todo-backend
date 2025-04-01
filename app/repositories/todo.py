from app.models.todo import Todo
from app.repositories.base import BaseRepository
from app.schema.todo import TodoCreate, TodoUpdate


class TodoRepository(BaseRepository[Todo, TodoCreate, TodoUpdate]):
    pass
