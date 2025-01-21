from uuid import UUID

from fastapi import APIRouter

from app.depends.user import UserIDDepends

router = APIRouter(prefix="/goals")


@router.get("")
async def get_goals(user_id: UserIDDepends):
    raise NotImplementedError


@router.get("/{goal_id}")
async def get_goal(user_id: UserIDDepends, goal_id: UUID):
    raise NotImplementedError


@router.post("")
async def create_goal(user_id: UserIDDepends):
    raise NotImplementedError


@router.patch("/{goal_id}")
async def update_goal(goal_id: UUID, user_id: UserIDDepends):
    raise NotImplementedError


@router.delete("/{goal_id}")
async def delete_goal(goal_id: UUID, user_id: UserIDDepends):
    raise NotImplementedError
