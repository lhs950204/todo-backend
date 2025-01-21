from sqlmodel import Session, select

from app.models.goal import Goal
from app.models.user import User


async def test_create_goal(session: Session):
    """목표 생성 테스트"""
    # 테스트용 사용자 생성
    user = User(email="test@example.com", name="test", hashed_password="dummy_hashed_password")
    session.add(user)
    session.commit()

    # 목표 생성
    goal = Goal(title="테스트 목표", user_id=user.id)
    session.add(goal)
    session.commit()
    session.refresh(goal)

    # 검증
    assert goal.id is not None
    assert goal.title == "테스트 목표"
    assert goal.user_id == user.id


async def test_update_goal(session: Session):
    """목표 수정 테스트"""
    # 테스트용 사용자와 목표 생성
    user = User(email="test@example.com", name="test", hashed_password="dummy_hashed_password")
    session.add(user)
    session.commit()

    goal = Goal(title="원래 목표", user_id=user.id)
    session.add(goal)
    session.commit()

    # 목표 수정
    goal.title = "수정된 목표"
    session.commit()
    session.refresh(goal)

    # 검증
    stmt = select(Goal).where(Goal.id == goal.id)
    updated_goal = session.exec(stmt).one()
    assert updated_goal.title == "수정된 목표"


async def test_delete_goal(session: Session):
    """목표 삭제 테스트"""
    # 테스트용 사용자와 목표 생성
    user = User(email="test@example.com", name="test", hashed_password="dummy_hashed_password")
    session.add(user)
    session.commit()

    goal = Goal(title="삭제할 목표", user_id=user.id)
    session.add(goal)
    session.commit()

    # 목표 삭제
    session.delete(goal)
    session.commit()

    # 검증
    stmt = select(Goal).where(Goal.id == goal.id)
    deleted_goal = session.exec(stmt).first()
    assert deleted_goal is None


async def test_query_user_goals(session: Session):
    """사용자의 목표 조회 테스트"""
    # 테스트용 사용자 생성
    user = User(email="test@example.com", name="test", hashed_password="dummy_hashed_password")
    session.add(user)
    session.commit()

    # 여러 목표 생성
    goals = [Goal(title=f"목표 {i}", user_id=user.id) for i in range(3)]
    session.add_all(goals)
    session.commit()

    # 사용자의 목표 조회
    stmt = select(Goal).where(Goal.user_id == user.id)
    user_goals = session.exec(stmt).all()

    # 검증
    assert len(user_goals) == 3
    assert all(goal.user_id == user.id for goal in user_goals)
    assert sorted([goal.title for goal in user_goals]) == ["목표 0", "목표 1", "목표 2"]


async def test_get_goal_by_id(session: Session):
    """ID로 목표 조회 테스트"""
    # 테스트용 사용자 생성
    user = User(email="test@example.com", name="test", hashed_password="dummy_hashed_password")
    session.add(user)
    session.commit()

    # 목표 생성
    goal = Goal(title="테스트 목표", user_id=user.id)
    session.add(goal)
    session.commit()

    # ID로 목표 조회
    stmt = select(Goal).where(Goal.id == goal.id)
    found_goal = session.exec(stmt).first()

    # 검증
    assert found_goal is not None
    assert found_goal.id == goal.id
    assert found_goal.title == goal.title
    assert found_goal.user_id == user.id
