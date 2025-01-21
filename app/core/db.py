from sqlmodel import create_engine

from app.core.settings import settings

engine = create_engine(str(settings.DB_URI), connect_args={"check_same_thread": False})
