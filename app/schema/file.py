import os

from pydantic import BaseModel

from app.core import settings


class FileCreate(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    mime_type: str
    size: int

    user_id: int


class FileUpdate(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    mime_type: str
    size: int


class FileSchema(FileCreate):
    id: int
