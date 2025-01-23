from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers import auth, goal, note, todo, user


# 임시코드임 나중에 alembic 으로 대체예정
@asynccontextmanager
async def lifespan(app: FastAPI):
    from sqlmodel import SQLModel

    from app.core.db import engine

    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(goal.router)
app.include_router(todo.router)
app.include_router(note.router)
