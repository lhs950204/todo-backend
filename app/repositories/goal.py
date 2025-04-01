from app.models.goal import Goal
from app.repositories.base import BaseRepository
from app.schema.goal import GoalCreate, GoalUpdate


class GoalRepository(BaseRepository[Goal, GoalCreate, GoalUpdate]):
    pass
