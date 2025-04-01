from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings

from .routers import auth, file, goal, note, todo, user


# 임시코드임 나중에 alembic 으로 대체예정
@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.db import engine
    from app.models.base import Base

    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=settings.MEDIA_ROOT), name="media")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(goal.router)
app.include_router(todo.router)
app.include_router(note.router)
app.include_router(file.router)
