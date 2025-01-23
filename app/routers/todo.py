from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func
from sqlmodel import delete, desc, select

from app.depends.db import SessionDep
from app.depends.user import UserIDDepends
from app.models.goal import Goal
from app.models.todo import Todo
from app.schema.todo import TodoCreate, TodoList, TodoProgress, TodoUpdate

router = APIRouter(prefix="/todos", tags=["Todo"])


@router.get("/", name="할 일 리스트 조회", response_model=TodoList)
async def get_todos(
    session: SessionDep,
    user_id: UserIDDepends,
    goal_id: int = Query(..., alias="goalId"),
    done: bool | None = Query(
        default=None,
        description="done이 true이면 완료된 todo만, false이면 미완료된 todo만 조회합니다. 아무것도 입력하지 않으면 모든 todo를 조회합니다.",
    ),
    cursor: int = Query(default=None, description="마지막으로 받은 할 일의 ID"),
    size: int = Query(default=20, gt=0),
):
    # 기본 쿼리 생성
    query = select(Todo).where(Todo.user_id == user_id, Todo.goal_id == goal_id)

    # done 필터 적용
    if done is not None:
        query = query.where(Todo.done == done)

    # 전체 할 일 수 조회
    total_count = session.scalar(
        select(func.count()).select_from(Todo).where(Todo.user_id == user_id, Todo.goal_id == goal_id)
    )
    assert total_count is not None

    # 커서 기반 페이지네이션
    if cursor:
        query = query.where(Todo.id <= cursor)

    # 정렬 및 제한
    query = query.order_by(desc(Todo.id)).limit(size + 1)

    todos = session.exec(query).all()

    # 다음 페이지 커서 설정
    next_cursor = None
    if len(todos) > size:
        next_cursor = todos[-1].id
        todos = todos[:size]

    return TodoList(todos=todos, next_cursor=next_cursor, total_count=total_count)


@router.post("/", name="할 일 생성", response_model=Todo)
async def create_todo(
    session: SessionDep,
    user_id: UserIDDepends,
    todo_create: TodoCreate,
):
    # goal이 현재 사용자의 것인지 확인
    goal = session.exec(select(Goal).where(Goal.id == todo_create.goal_id, Goal.user_id == user_id)).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    new_todo = Todo(
        title=todo_create.title,
        link_url=todo_create.link_url,
        file_url=todo_create.file_url,
        user_id=user_id,
        goal_id=todo_create.goal_id,
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


@router.get("/progress", name="할 일 진행 상황 조회", response_model=TodoProgress)
async def get_todo_progress(session: SessionDep, user_id: UserIDDepends, goal_id: int = Query(..., alias="goalId")):
    # 전체 할 일 수
    total = session.scalar(
        select(func.count()).select_from(Todo).where(Todo.user_id == user_id, Todo.goal_id == goal_id)
    )
    assert total is not None

    # 완료된 할 일 수
    completed = session.scalar(
        select(func.count())
        .select_from(Todo)
        .where(Todo.user_id == user_id, Todo.goal_id == goal_id, Todo.done == True)
    )
    assert completed is not None

    # 완료율 계산
    completion_rate = (completed / total * 100) if total > 0 else 0.0

    return TodoProgress(
        total=total,
        completed=completed,
        completion_rate=completion_rate,
    )


@router.get("/{todo_id}", name="할 일 상세 조회", response_model=Todo)
async def get_todo(
    session: SessionDep,
    user_id: UserIDDepends,
    todo_id: int,
):
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.patch("/{todo_id}", name="할 일 수정", response_model=Todo)
async def update_todo(
    session: SessionDep,
    user_id: UserIDDepends,
    todo_id: int,
    todo_update: TodoUpdate,
):
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # goal_id가 변경되는 경우, 새로운 goal이 현재 사용자의 것인지 확인
    if todo_update.goal_id is not None:
        goal = session.exec(select(Goal).where(Goal.id == todo_update.goal_id, Goal.user_id == user_id)).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

    todo_data = todo_update.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo, key, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.delete("/{todo_id}", name="할 일 삭제", status_code=204)
async def delete_todo(session: SessionDep, user_id: UserIDDepends, todo_id: int):
    result = session.exec(delete(Todo).where(Todo.id == todo_id, Todo.user_id == user_id))

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.commit()
