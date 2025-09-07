# app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Snippet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[str] = None  # store comma-separated tags for simplicity
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: Optional[str] = None
