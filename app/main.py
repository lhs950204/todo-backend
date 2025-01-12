from typing import Optional, Union

from fastapi import FastAPI, Path, Query, UploadFile

from .routers import auth, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
