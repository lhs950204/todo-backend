from app.models.note import Note
from app.repositories.base import BaseRepository
from app.schema.note import NoteCreate, NoteUpdate


class NoteRepository(BaseRepository[Note, NoteCreate, NoteUpdate]):
    pass
