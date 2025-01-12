from contextlib import asynccontextmanager
from typing import Optional, Union

from fastapi import FastAPI, Path, Query, UploadFile

from .routers import auth, user


# 임시코드임 나중에 alembic 으로 대체예정
@asynccontextmanager
async def lifespan(app: FastAPI):
    from sqlmodel import SQLModel

    from app.core.db import engine

    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
