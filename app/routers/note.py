from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func
from sqlmodel import delete, desc, select

from app.depends.db import SessionDep
from app.depends.user import UserIDDepends
from app.models.goal import Goal
from app.models.note import Note
from app.schema.note import NoteCreate, NoteList, NoteUpdate

router = APIRouter(prefix="/notes", tags=["Note"])


@router.get("", name="노트 리스트 조회", response_model=NoteList)
async def get_notes(
    session: SessionDep,
    user_id: UserIDDepends,
    goal_id: int,
    cursor: int = Query(default=None, description="마지막으로 받은 노트의 ID"),
    size: int = Query(default=20, gt=0),
):
    # 전체 노트 수 조회
    total_count = session.scalar(
        select(func.count()).select_from(Note).where(Note.user_id == user_id, Note.goal_id == goal_id)
    )
    assert total_count is not None

    # 기본 쿼리 생성
    query = select(Note).where(Note.user_id == user_id, Note.goal_id == goal_id)

    # 커서 기반 페이지네이션
    if cursor:
        query = query.where(Note.id <= cursor)

    # 정렬 및 제한
    query = query.order_by(desc(Note.id)).limit(size + 1)

    notes = session.exec(query).all()

    # 다음 페이지 커서 설정
    next_cursor = None
    if len(notes) > size:
        next_cursor = notes[-1].id
        notes = notes[:size]

    return NoteList(notes=notes, next_cursor=next_cursor, total_count=total_count)


@router.post("", name="노트 생성", response_model=Note)
async def create_note(session: SessionDep, user_id: UserIDDepends, note: NoteCreate):
    # goal이 현재 사용자의 것인지 확인
    goal = session.exec(select(Goal).where(Goal.id == note.goal_id, Goal.user_id == user_id)).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    new_note = Note(
        title=note.title,
        content=note.content,
        link_url=note.link_url,
        user_id=user_id,
        goal_id=note.goal_id,
        todo_id=note.todo_id,
    )
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    return new_note


@router.get("/{note_id}", name="노트 조회", response_model=Note)
async def get_note(session: SessionDep, user_id: UserIDDepends, note_id: int):
    note = session.exec(select(Note).where(Note.id == note_id, Note.user_id == user_id)).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.patch("/{note_id}", name="노트 수정", response_model=Note)
async def update_note(session: SessionDep, user_id: UserIDDepends, note_id: int, note: NoteUpdate):
    db_note = session.exec(select(Note).where(Note.id == note_id, Note.user_id == user_id)).first()

    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_data = note.model_dump(exclude_unset=True)
    for key, value in note_data.items():
        setattr(db_note, key, value)

    session.add(db_note)
    session.commit()
    session.refresh(db_note)

    return db_note


@router.delete("/{note_id}", name="노트 삭제", status_code=204)
async def delete_note(session: SessionDep, user_id: UserIDDepends, note_id: int):
    result = session.exec(delete(Note).where(Note.id == note_id, Note.user_id == user_id))

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")

    session.commit()
