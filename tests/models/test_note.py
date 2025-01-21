import pytest
from sqlmodel import Session, select

from app.models.note import Note
from app.models.user import User
from app.models.goal import Goal
from app.models.todo import Todo


async def test_create_note(session: Session, default_user: User, default_goal: Goal, default_todo: Todo):
    note = Note(
        title="새로운 노트",
        content="노트 내용",
        link_url="https://test.com",
        user_id=default_user.id,
        goal_id=default_goal.id,
        todo_id=default_todo.id,
    )
    session.add(note)
    session.commit()
    session.refresh(note)

    assert note.id is not None
    assert note.title == "새로운 노트"
    assert note.content == "노트 내용"
    assert note.link_url == "https://test.com"
    assert note.user_id == default_user.id
    assert note.goal_id == default_goal.id
    assert note.todo_id == default_todo.id


async def test_read_note(session: Session, default_note: Note):
    db_note = session.exec(select(Note).where(Note.id == default_note.id)).one()

    assert db_note.id == default_note.id
    assert db_note.title == default_note.title
    assert db_note.content == default_note.content
    assert db_note.link_url == default_note.link_url


async def test_update_note(session: Session, default_note: Note):
    default_note.title = "수정된 노트"
    default_note.content = "수정된 내용"
    session.add(default_note)
    session.commit()
    session.refresh(default_note)

    updated_note = session.exec(select(Note).where(Note.id == default_note.id)).one()

    assert updated_note.title == "수정된 노트"
    assert updated_note.content == "수정된 내용"


async def test_delete_note(session: Session, default_note: Note):
    session.delete(default_note)
    session.commit()

    deleted_note = session.exec(select(Note).where(Note.id == default_note.id)).first()

    assert deleted_note is None


async def test_note_relationships(
    session: Session, default_note: Note, default_user: User, default_goal: Goal, default_todo: Todo
):
    db_note = session.exec(select(Note).where(Note.id == default_note.id)).one()

    assert db_note.user.id == default_user.id
    assert db_note.goal.id == default_goal.id
    assert db_note.todo.id == default_todo.id

    db_user = session.exec(select(User).where(User.id == default_user.id)).one()

    assert db_user.notes[0].id == default_note.id
