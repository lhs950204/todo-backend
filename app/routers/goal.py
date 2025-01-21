from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func
from sqlmodel import asc, delete, desc, select

from app.depends.db import SessionDep
from app.depends.user import UserIDDepends
from app.models.goal import Goal
from app.schema.common import SortOrder
from app.schema.goal import GoalCreate, GoalList, GoalUpdate

router = APIRouter(prefix="/goals", tags=["Goal"])


@router.get("", name="내 목표 리스트 조회", response_model=GoalList)
async def get_goals(
    session: SessionDep,
    user_id: UserIDDepends,
    cursor: int = Query(default=None, description="마지막으로 받은 목표의 ID"),
    size: int = Query(default=20, gt=0),
    sort_order: SortOrder = Query(default=SortOrder.DESC, alias="sortOrder"),
):
    total_count = session.scalar(select(func.count()).select_from(Goal).where(Goal.user_id == user_id))
    assert total_count is not None

    query = select(Goal).where(Goal.user_id == user_id)

    # 커서 기반 페이지네이션
    if cursor:
        if sort_order == SortOrder.DESC:
            query = query.where(Goal.id <= cursor)
        else:
            query = query.where(Goal.id >= cursor)

    # 정렬
    if sort_order == SortOrder.DESC:
        query = query.order_by(desc(Goal.id))
    else:
        query = query.order_by(asc(Goal.id))

    # 사이즈 제한
    query = query.limit(size + 1)  # 다음 페이지 존재 여부 확인을 위해 1개 더 가져옴

    goals = session.exec(query).all()

    # 다음 페이지 커서 설정
    next_cursor = None
    if len(goals) > size:
        next_cursor = goals[-1].id
        goals = goals[:size]

    # 전체 목표 수 조회

    return GoalList(goals=goals, next_cursor=next_cursor, total_count=total_count)


@router.post("", name="내 목표 생성", response_model=Goal)
async def create_goal(session: SessionDep, user_id: UserIDDepends, goal: GoalCreate):
    new_goal = Goal(
        title=goal.title,
        user_id=user_id,
    )
    session.add(new_goal)
    session.commit()
    session.refresh(new_goal)
    return new_goal


@router.get("/{goal_id}", name="내 목표 조회", response_model=Goal)
async def get_goal(session: SessionDep, user_id: UserIDDepends, goal_id: int):
    goal = session.exec(select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    return goal


@router.patch("/{goal_id}", name="내 목표 수정", response_model=Goal)
async def update_goal(session: SessionDep, goal_id: int, user_id: UserIDDepends, goal: GoalUpdate):
    db_goal = session.exec(select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id)).first()

    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # 업데이트할 필드 설정
    goal_data = goal.model_dump(exclude_unset=True)
    for key, value in goal_data.items():
        setattr(db_goal, key, value)

    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)

    return db_goal


@router.delete("/{goal_id}", name="내 목표 삭제", status_code=204)
async def delete_goal(session: SessionDep, goal_id: int, user_id: UserIDDepends) -> None:
    result = session.exec(delete(Goal).where(Goal.id == goal_id, Goal.user_id == user_id))

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Goal not found")

    session.commit()
