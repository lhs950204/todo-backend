from datetime import datetime, timezone

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class ModelBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
