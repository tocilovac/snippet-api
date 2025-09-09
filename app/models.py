from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Snippet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[str] = None  # comma-separated tags
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
